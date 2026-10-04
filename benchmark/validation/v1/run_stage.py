"""Run one validation stage's batches through its agent CLI.

Each batch is sent headless to the stage's runner with the stage brief, the
reply is checked against the stage schema and the batch's case IDs, quotes are
checked against the article text, and the transcript is scanned for access to
gold locations. Without --execute nothing is called: the commands are printed.
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from stage0 import HERE, load

STAGES = {  # stage -> brief, schema, read tools for the Claude runner, blind
    "stage1_blind": ("stage1_blind.md", "stage1_blind.schema.json", "Read Grep Glob", True),
    "stage2_audit": ("stage2_audit.md", "stage2_audit.schema.json", "Read Grep Glob", False),
    "stage3_hunt": ("stage3_hunt.md", "stage3_hunt.schema.json", "Read Grep Glob", False),
    "stage4_compare": ("stage4_compare.md", "stage4_compare.schema.json", "Read", False),
    "stage5_adjudicate": ("stage5_adjudicate.md", "stage5_adjudicate.schema.json", "Read Grep Glob", False),
}
# A blind run that names any of these has looked outside its workspace at gold.
GOLD_MARKERS = ("benchmark/", "golden_qa", "jua-106-gold-ws", "jua-106-seeds",
                "ai-research-assistant", "corpus/JUA-106", "queries.json")
MAX_ATTEMPTS = 2


def normalise(text: str) -> str:
    return " ".join(text.split())


def schema_errors(value, schema: dict, path: str = "$") -> list[str]:
    """Validate the subset of JSON Schema the stage schemas use."""
    kind = schema.get("type")
    if kind == "object":
        if not isinstance(value, dict):
            return [f"{path}: expected object"]
        errors = [f"{path}: missing {k}" for k in schema.get("required", []) if k not in value]
        errors += [f"{path}: unexpected {k}" for k in value if k not in schema["properties"]]
        for key, sub in schema["properties"].items():
            if key in value:
                errors += schema_errors(value[key], sub, f"{path}.{key}")
        return errors
    if kind == "array":
        if not isinstance(value, list):
            return [f"{path}: expected array"]
        return [e for i, item in enumerate(value) for e in schema_errors(item, schema["items"], f"{path}[{i}]")]
    if kind == "boolean":
        return [] if isinstance(value, bool) else [f"{path}: expected boolean"]
    if not isinstance(value, str):
        return [f"{path}: expected string"]
    if "enum" in schema and value not in schema["enum"]:
        return [f"{path}: {value!r} not in {schema['enum']}"]
    return []


def strings(value):
    if isinstance(value, str):
        yield value
    elif isinstance(value, dict):
        for item in value.values():
            yield from strings(item)
    elif isinstance(value, list):
        for item in value:
            yield from strings(item)


def dicts(value):
    if isinstance(value, dict):
        yield value
        for item in value.values():
            yield from dicts(item)
    elif isinstance(value, list):
        for item in value:
            yield from dicts(item)


def extract_replies(transcript: str, key: str) -> list[dict]:
    """Every JSON object carrying `key`, wherever the CLI's event format put it."""
    events = []
    for line in transcript.splitlines():
        try:
            events.append(json.loads(line))
        except json.JSONDecodeError:
            events.append(line)
    found, decoder = [], json.JSONDecoder()
    for event in events:
        found += [c for c in dicts(event) if key in c]
        for text in strings(event):
            if f'"{key}"' not in text:
                continue
            for match in re.finditer(r"\{", text):
                try:
                    candidate, _ = decoder.raw_decode(text[match.start():])
                except json.JSONDecodeError:
                    continue
                if isinstance(candidate, dict) and key in candidate:
                    found.append(candidate)
                    break
    return found


def pick_reply(candidates: list[dict], schema: dict):
    """Last schema-valid candidate; a batch file echoed in the transcript is not one."""
    valid = [c for c in candidates if not schema_errors(c, schema)]
    return (valid or candidates or [None])[-1]


def usage_records(transcript: str) -> list[dict]:
    records = []
    for line in transcript.splitlines():
        try:
            event = json.loads(line)
        except json.JSONDecodeError:
            continue
        for item in dicts(event):
            for key, value in item.items():
                if "usage" in key.lower() and isinstance(value, dict):
                    records.append(value)
    return records[-3:]


def command(runner: dict, prompt: str, cwd: Path, schema_path: Path, tools: str,
            reply_path: Path, overrides: dict) -> tuple[list[str], str | None]:
    """Argument list and stdin for one headless call."""
    cli = runner["cli"]
    binary = overrides.get(cli, cli)
    if cli == "kimi":
        return [binary, "-m", runner["model"], "--output-format", "stream-json", "-p", prompt], None
    if cli == "codex":
        return [binary, "exec", "-m", runner["model"],
                "-c", f'model_reasoning_effort="{runner["reasoning_effort"]}"',
                "-s", "read-only", "-C", str(cwd), "--skip-git-repo-check", "--ephemeral", "--json",
                "--output-schema", str(schema_path), "-o", str(reply_path), "-"], prompt
    if cli == "claude":
        return [binary, "-p", "--model", runner["model"], "--restricted", "--tools", *(tools.split() or [""]),
                "--strict-mcp-config", "--no-session-persistence", "--output-format", "stream-json",
                "--verbose", "--json-schema", schema_path.read_text(encoding="utf-8")], prompt
    raise ValueError(f"unknown runner {cli}")


def check_quotes(reply, articles: Path) -> dict:
    """Mark every {file, quote} pair with whether the quote is in that file."""
    cache, verified, total = {}, 0, 0
    for item in dicts(reply):
        if not (isinstance(item.get("file"), str) and isinstance(item.get("quote"), str)):
            continue
        if not item["quote"]:
            continue
        total += 1
        name = Path(item["file"]).name
        if name not in cache:
            path = articles / name
            cache[name] = normalise(path.read_text(encoding="utf-8")) if path.is_file() else None
        item["quote_verified"] = bool(cache[name]) and normalise(item["quote"]) in cache[name]
        verified += item["quote_verified"]
    return {"verified": verified, "total": total}


def run_batch(batch: dict, stage: str, runner: dict, args, schema: dict) -> dict:
    brief, schema_name, tools, blind = STAGES[stage]
    batch_path = args.workspace_root / batch["batch_file"]
    cwd = batch_path.parent.parent
    placeholder = "{case_file}" if stage == "stage5_adjudicate" else "{batch_file}"
    prompt = (HERE / "briefs" / brief).read_text(encoding="utf-8").replace(
        placeholder, f"{batch_path.parent.name}/{batch_path.name}")
    result_path = args.results_dir / f"{batch['batch_id']}.json"
    run_dir = args.workspace_root / "jua-106-runs" / args.group
    if result_path.exists():
        return {"batch_id": batch["batch_id"], "status": "kept"}
    key = "verdict" if stage == "stage5_adjudicate" else "cases"
    problems = []
    for attempt in range(1, MAX_ATTEMPTS + 1):
        transcript_path = run_dir / f"{batch['batch_id']}.attempt{attempt}.transcript"
        reply_path = run_dir / f"{batch['batch_id']}.attempt{attempt}.reply.json"
        argv, stdin = command(runner, prompt, cwd, HERE / "schemas" / schema_name, tools, reply_path, args.cli)
        if not args.execute:
            shown = [a if len(a) < 120 else f"<{len(a)} chars>" for a in argv]
            return {"batch_id": batch["batch_id"], "status": "dry_run", "cwd": str(cwd), "command": shown}
        run_dir.mkdir(parents=True, exist_ok=True)
        started = time.time()
        try:
            done = subprocess.run(argv, input=stdin, cwd=cwd, capture_output=True, text=True, timeout=args.timeout)
            transcript = done.stdout + ("\n" + done.stderr if done.stderr else "")
        except subprocess.TimeoutExpired as error:
            transcript = f"{error.stdout or ''}\nTIMEOUT after {args.timeout}s"
        transcript_path.write_text(transcript, encoding="utf-8")
        reply = load(reply_path) if reply_path.is_file() else pick_reply(extract_replies(transcript, key), schema)
        if reply is None:
            problems.append(f"attempt {attempt}: no JSON reply found")
            continue
        errors = schema_errors(reply, schema)
        expected = batch["cases"]
        got = [reply.get("id")] if stage == "stage5_adjudicate" else [c.get("id") for c in reply.get("cases", []) if isinstance(c, dict)]
        if sorted(got) != sorted(expected):
            errors.append(f"case ids {sorted(got)} differ from batch {sorted(expected)}")
        leaked = sorted(m for m in GOLD_MARKERS if m in transcript) if blind else []
        if leaked:
            errors.append(f"blind run referenced gold locations: {leaked}")
        if errors:
            problems.append(f"attempt {attempt}: " + "; ".join(errors[:8]))
            continue
        record = {
            "batch_id": batch["batch_id"], "stage": stage, "group": args.group, "runner": runner,
            "attempts": attempt, "earlier_problems": problems, "duration_s": round(time.time() - started, 1),
            "quotes": check_quotes(reply, cwd / "articles"), "usage": usage_records(transcript),
            "transcript": str(transcript_path.relative_to(args.workspace_root)), "output": reply,
        }
        args.results_dir.mkdir(parents=True, exist_ok=True)
        result_path.write_text(json.dumps(record, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        result_path.with_suffix(".gap.json").unlink(missing_ok=True)
        return {"batch_id": batch["batch_id"], "status": "ok", "attempts": attempt, "quotes": record["quotes"]}
    gap = {"batch_id": batch["batch_id"], "stage": stage, "group": args.group, "cases": batch["cases"],
           "status": "unreviewed", "problems": problems}
    args.results_dir.mkdir(parents=True, exist_ok=True)
    (args.results_dir / f"{batch['batch_id']}.gap.json").write_text(json.dumps(gap, indent=2) + "\n", encoding="utf-8")
    return {"batch_id": batch["batch_id"], "status": "gap", "problems": problems}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--group", required=True,
                        help="Batch group: a key of manifest.json batches, or a label for --batch-list")
    parser.add_argument("--batch-list", type=Path,
                        help="JSON file mapping stage to batches, for groups built outside the manifest")
    parser.add_argument("--stage", choices=sorted(STAGES), help="Stage; inferred from a manifest group name")
    parser.add_argument("--runner", help="Runner key in manifest.json; defaults to the group or stage name")
    parser.add_argument("--workspace-root", type=Path, required=True)
    parser.add_argument("--results-dir", type=Path, help="Defaults to results/<group> beside this script")
    parser.add_argument("--only", nargs="*", help="Batch IDs to run; default all in the group")
    parser.add_argument("--jobs", type=int, default=1)
    parser.add_argument("--timeout", type=int, default=3600, help="Seconds per attempt")
    parser.add_argument("--cli", nargs="*", default=[], metavar="NAME=PATH", help="Substitute a CLI binary")
    parser.add_argument("--execute", action="store_true", help="Call the CLI; without it, print the commands")
    args = parser.parse_args()
    args.workspace_root = args.workspace_root.resolve()
    args.cli = dict(item.split("=", 1) for item in args.cli)
    args.results_dir = args.results_dir or HERE / "results" / args.group

    manifest = load(HERE / "manifest.json")
    stage = args.stage or args.group.removeprefix("pilot_")
    stage = "stage1_blind" if stage == "stage1_double" else stage
    if stage not in STAGES:
        raise SystemExit(f"cannot infer stage from group {args.group!r}; pass --stage")
    batches = load(args.batch_list)[stage] if args.batch_list else manifest["batches"][args.group]
    if args.only:
        batches = [b for b in batches if b["batch_id"] in args.only]
    runner_key = args.runner or (args.group if args.group in manifest["runners"] else stage)
    runner = manifest["runners"][runner_key]
    schema = load(HERE / "schemas" / STAGES[stage][1])

    with ThreadPoolExecutor(max_workers=args.jobs) as pool:
        outcomes = list(pool.map(lambda b: run_batch(b, stage, runner, args, schema), batches))
    for outcome in outcomes:
        print(json.dumps(outcome, ensure_ascii=False))
    counts = {s: sum(1 for o in outcomes if o["status"] == s) for s in ("ok", "kept", "gap", "dry_run")}
    print(json.dumps({"group": args.group, "stage": stage, "runner": runner_key, **counts}))


if __name__ == "__main__":
    main()
