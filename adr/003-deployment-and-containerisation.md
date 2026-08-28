# ADR-003: Deployment and Containerisation

## Context

Production-readiness for `ai-research-assistant` started at roughly
2/10 — no health check, no way to run it without a hand-built local
environment, blocking model loads baked into request handling. This
ADR covers the containerisation slice that lifts that floor, and — more
importantly — what was deliberately left undone and why.

The scope was fixed in advance and timeboxed to ~2 days. The job search
is active and the CV is going out; the evaluation harness, the measured
null results on BM25/rewriting, and the honest ADRs are the actual
differentiators in this portfolio. Containerisation removes a visible
negative. It is not itself meant to be the differentiator, so the
target here is a defensible 6/10, not a 10/10.

## Decisions made

**Background model loading via a lifespan background task, not a
synchronous startup.** `_startup()` runs in a worker thread
(`asyncio.create_task(asyncio.to_thread(_startup))`) launched from
FastAPI's `lifespan`, which returns immediately. This matters
mechanically, not just stylistically: uvicorn does not accept
connections until `lifespan` startup returns. A synchronous startup
would mean `/health` never has an observable "loading" state to
report — requests would simply not be accepted at all until models
finished loading, making the health check decorative. The background
task is what makes "loading → ready" a real, checkable transition
instead of a binary up/down.

**Named Docker volume for Chroma, not a bind mount.** `chroma_data:/data/chroma_db`
in `docker-compose.yml`, with `CHROMA_PATH` read from the environment
(defaulting to `./chroma_db` so local, non-Docker development is
unchanged). A bind mount to `./chroma_db` was considered and rejected —
it ties the deployment artifact to host-specific paths and permissions,
which is exactly the kind of "works on my machine" fragility a
containerised deliverable is supposed to remove. A named volume is
portable across whichever machine runs `docker compose up`.

**Model weights baked into the image at build time, with
`HF_HUB_OFFLINE=1` at runtime.** The Dockerfile runs an inline
`RUN python -c "..."` that constructs both the FastEmbed embedding
model and the cross-encoder reranker during the build, directly below
the `COPY main.py .` line, with a comment flagging that a model-name
change in `main.py` needs a matching Dockerfile update. This is a
determinism choice, not a speed one: with `HF_HUB_OFFLINE=1` set, a
build-time/runtime cache-path mismatch fails loudly (the process can't
reach the Hugging Face CDN and errors out) instead of silently falling
back to a slow, network-dependent re-download on first request.

**Healthcheck via `python -c "urllib.request.urlopen(...)"`, not `curl`.**
Avoids installing an extra system package into the image for a single
HTTP GET that the Python interpreter — already present — can make
directly.

**Single `/health` endpoint, not a Kubernetes-style liveness/readiness
split.** `/health` returns `503` with `{"status": "loading"}` while
models are loading, `503` with the startup error if loading failed, and
`200` with the current chunk count once ready. A liveness/readiness
split exists to answer two different orchestrator questions — "should
this container be restarted" vs. "should traffic be routed to it" —
and there is no orchestrator here to ask either question. One endpoint
answering "is this usable yet" is the right amount of health check for
a `docker compose up` demo target.

**`PYTHONUNBUFFERED=1` in the image.** Python line-buffers stdout when
it isn't attached to a TTY, which is always the case inside a
container. Without this, the `[startup]` progress logging in `main.py`
buffers and never reaches `docker compose logs`, so the loading → ready
sequence the health check exposes has no visible narration alongside
it. Found after JUA-32's verification pass, which checked `/health`
status transitions but not log output.

**Module-level globals over `app.state`.** `embed_model`, `reranker`,
`chroma_client`, `collection`, `llm`, and the BM25 index are module
globals, set once by `_startup()`. `app.state` is the more idiomatic
FastAPI pattern for request-scoped or test-injectable state, and was
considered — but this service runs as a single process with no
multi-app or test-fixture need to inject a different set of models per
instance, so the extra indirection buys nothing here.

**A bounded LLM attempt, with retries owned by the caller.** The grounded
answer call has a 35-second timeout and the opt-in query rewrite, capped at
100 tokens, has its own 10-second timeout. The Anthropic client is configured
with `max_retries=0`; an `APITimeoutError` from either call becomes an HTTP
`504` rather than an unclassified `500`. This keeps the worst-case inner
budget below the gateway's 60-second read timeout, including when rewriting
causes two sequential LLM calls. Warm Docker measurements against the four
document seed corpus on 27 Aug 2026 were 3.07–4.37 seconds for three baseline
queries and 5.98–9.01 seconds for two rewrite-enabled queries. The chosen
limits therefore leave about 15 seconds for retrieval, reranking, and response
handling in the worst rewrite case, while remaining well above observed
latency.

The retry owner is the gateway because it owns the user-facing latency budget
and can circuit-break. Allowing both the Anthropic SDK and the gateway to make
two retries could multiply into nine LLM attempts for one user request. A
caller retry repeats embedding, Chroma retrieval, reranking, and generation,
whereas an SDK retry would repeat only generation; that extra local work is
accepted in exchange for one visible retry budget with one owner. The
provider failures the SDK retries before generation do not consume output
tokens, so this does not add token cost.

**The 1,024-token grounded-answer cap stays unchanged.** Observed MCP
Inspector answers were roughly 130–200 tokens, about 20% of the cap. If a
generation reaches the cap during structured output, parsing can fail
deterministically and a caller may spend its retry budget on a failure that
cannot succeed. That gap is accepted for now; increasing the cap is the lever
if it appears. The system prompt was deliberately left unchanged because its
wording underpins the existing `context_sufficient` accuracy measurements.
The model remains pinned to the dated `claude-haiku-4-5-20251001` snapshot so
provider alias changes cannot silently alter those measured behaviours.

**Readiness excludes the LLM round-trip.** `_ready = True` is set once
models are loaded, Chroma is connected, the BM25 index is built, and
seeding (if applicable) is complete — it does not send a live request
to the LLM provider first. A "ready" service can therefore still fail
an actual `/query` call if the Anthropic API is unreachable or the key
is invalid. This is a deliberate scope boundary: verifying live
third-party API connectivity as part of the readiness check is a
different, larger piece of work (timeouts, retry policy, what "ready"
should mean if the provider is degraded but not down), and out of
scope for this timebox.

**Query validation is API hygiene, not prompt-injection mitigation.**
`question` is stripped and bounded to 1–1,000 characters, while `n_results`
is bounded to 1–`FUSED_CANDIDATE_POOL`. These limits contain cost, reject
meaningless requests with a clear `422`, and make the retrieval contract
explicit. They do not make natural-language input safe from prompt injection:
there is nothing reliable to escape or filter, and phrase blocklists are
defeated by rewording.

The localhost, unauthenticated service has no privilege boundary between the
question author and the operator. Its existing design still limits impact:
the LLM has no tools, filesystem, or network access; structured output limits
the response shape; and `sources` comes from retrieval rather than from the
model, so an injected answer cannot fabricate citations. A question can still
coerce the model into setting `context_sufficient=true` for a fabricated
answer. That is a known limitation, not a vulnerability in the current trust
model. The material future threat is indirect injection from an untrusted
ingested document, particularly if `/ingest` becomes publicly reachable; that
risk belongs alongside the authentication and rate-limiting work in JUA-28.

## Deliberately not built

These were considered and rejected, not simply skipped — the
distinction matters, because undocumented gaps read as unawareness and
documented-and-deliberate reads as judgement.

- **No cloud deployment.** Decided against on 17 Aug 2026. The service
  holds an Anthropic API key. An unauthenticated public endpoint with a
  live API key behind it is an open wallet — anyone who finds the URL
  can spend against it. Protecting that properly (API-key auth, rate
  limiting, a spend cap) is roughly a week of work to guard a demo
  nobody asked to be permanently live. `docker compose up` on a
  reviewer's own machine is the deliverable; it doesn't need a public
  URL to prove the point.
- **No CI pipeline in this timebox.** A build-and-smoke-test GitHub
  Actions workflow is parked as a nice-to-have (JUA-34, low priority),
  to be picked up only after the core three issues in this epic are
  done. `docker compose up` on a clean clone is complete without it.
- **No API-key auth or rate limiting on the endpoints themselves**
  (tracked separately as JUA-28) — consistent with, and for the same
  reason as, the no-cloud-deployment decision above: this only becomes
  necessary once something is reachable over the network from outside
  the operator's own machine.
- **No orchestration** (Kubernetes, ECS, etc.) — there is exactly one
  service and one dependency (Chroma, embedded in-process); an
  orchestrator would be solving a problem this deployment doesn't have.
- **Root user, no `HF_HOME` override.** The image runs as root, and
  build-time and runtime Hugging Face cache paths match only because
  both run as the same user. This is a real trade-off, not an
  oversight: a non-root user with an explicit `HF_HOME` is the more
  correct pattern, but security hardening was explicitly scoped out of
  this epic, and revisiting user/permissions here without also
  addressing auth would fix the smaller problem while leaving the
  bigger one (an open API key) untouched.
- **No evaluation tooling shipped in the image.** `eval_golden.py`,
  `golden_qa.json`, and `corpus_manifest.json` are not copied into the
  container. Evaluation is, and remains, a host-side workflow run
  against the full 19-document corpus — the seed corpus baked into the
  image is a demo aid, not something ever run through the eval harness
  (see "Consequences" below).

## Consequences

- A reviewer can go from a clean clone to a working, queryable service
  in one command, with an honest loading → ready transition and data
  that survives a restart (`docker compose restart` reuses the named
  volume; seeding is skipped once the collection is non-empty).
- The seed corpus (4 CC-BY-licensed articles, 429 chunks) exists purely
  so the container isn't empty on first run. It has never been run
  through `eval_golden.py` and is not represented in the 96.4% (n=3) /
  98.2% (n=8) figures reported elsewhere in this repo — those numbers
  belong to the full 19-document corpus, loaded separately via
  `ingest_corpus.py` against a host-run (non-Docker) instance. The
  README quickstart states this explicitly so the two corpora are never
  conflated.
- **`docker-compose.yml` pins `SEED_ON_EMPTY` and `CHROMA_PATH` via
  `environment:`, which Compose resolves with higher precedence than
  `env_file:`.** Originally both values reached the container only
  through `env_file: .env`, so a developer's local `.env` — tuned for
  host development, where `SEED_ON_EMPTY=false` avoids seed/full-corpus
  contamination (see below) — silently reached the reviewer's container
  too, either skipping the demo seed or, if `CHROMA_PATH` diverged,
  writing Chroma data outside the mounted volume and breaking the
  persistence this ADR documents. Verified via `docker compose config`:
  the reviewer path now shows `SEED_ON_EMPTY=true` and
  `CHROMA_PATH=/data/chroma_db` regardless of what's set locally.
  `.env.example`'s comments were updated to state this rather than warn
  against a hazard that no longer exists.
- **The host development path must independently set
  `SEED_ON_EMPTY=false`.** The seed corpus and the full 19-document
  corpus share four overlapping articles (see
  `seed_corpus/ATTRIBUTION.md`) — if the host server auto-seeds before
  `ingest_corpus.py` runs, those four end up ingested twice under
  different filenames (`.txt` from the seed corpus, `.pdf`-derived from
  the full corpus). `eval_golden.py`'s document-name matching can't
  deduplicate that, so it would silently corrupt retrieval evaluation.
  Previously this was documented only in `seed_corpus/ATTRIBUTION.md`;
  it's now stated directly in the README's host section.
- Because readiness doesn't probe the LLM provider, a misconfigured or
  invalid `ANTHROPIC_API_KEY` will not be visible at `/health` — it
  surfaces only on the first `/query` call, as a request-level error.
  Worth knowing if `/health` reports `200` but queries still fail.
