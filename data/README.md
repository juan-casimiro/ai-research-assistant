# Current corpus and research evidence

The current frozen corpus is **V2: 55 articles and 158 evaluation questions**.
[manifest.json](manifest.json) is its source of truth and records
`corpus_version: combined-selection-v2`. PDFs and extracted text are downloaded
or prepared locally under the ignored `corpus/` directory.

| Location | Contents |
| --- | --- |
| [manifest.json](manifest.json) | Current frozen article inventory and pinned versions/hashes |
| [benchmark/](benchmark/README.md) | Topic questions, conditions, dependencies, selection records and readable cases |
| [evaluations/](evaluations/) | Saved retrieval runs, analysis and provenance |
| [findings/](findings/retrieval.md) | Reports interpreting this version's results and limitations |
| [archive/v1/](archive/v1/) | Original 19-article manifest, 133-question gold and five evaluation outputs, with their original schemas |
| [archive/development/](archive/development/) | Superseded combined experiment and retained review evidence |

Generic development utilities live separately in [tools/](../tools/README.md).
Repository decisions remain under [adr/](../adr/); the
[benchmark standards](../docs/benchmark-standards.md) apply across versions. The [release scope and file inventory](../docs/release-scope.md)
explain which current and historical evidence is retained and why.

When a new corpus is frozen, move the current manifest, benchmark, evaluations
and findings together into `archive/v2/` and put the new current version here. Update the destination paths in
`layout.json` for the moved frozen records, retaining their original hashes.
Keep each archived version's original structure/schema; do not normalize old
records to the new schema. Topic source directories called `v1` are authoring
records used by the current corpus, rather than the original 19-article corpus.

## Download, ingest and evaluate

From the repository root, using its Python 3.12 environment:

```sh
python -m tools.corpus.download_corpus --manifest data/manifest.json --corpus-dir corpus/combined-v2
# Start the service with SEED_ON_EMPTY=false and a fresh CHROMA_PATH first.
python -m tools.corpus.ingest_corpus --manifest data/manifest.json --corpus-dir corpus/combined-v2
python -m tools.evaluation.eval_golden --benchmark data/benchmark/cardiology \
  --corpus-dir corpus/combined-v2 --condition C3 --output data/evaluations/local/cardio.json
```

These commands create a new experiment. Retrieval evaluation verifies pinned
PDF/text bytes and actual collection membership; a fresh run uses the adapted
utility's source fingerprint and cannot be relabelled as the sealed experiment.
[Tool guidance](../tools/README.md) explains prerequisites and historical replay.
Downloading current PMC bytes is not guaranteed to recreate the historical bytes
pinned in the manifest, even when the PMC deposit version is unchanged.

## Verify the retained experiment

[layout.json](layout.json) records every original path, destination and pre-move
SHA-256. Frozen manifests, gold, metadata, results, seals and historical helper
bytes are unchanged. Their recorded paths remain in the original namespace.
The replay runner checks relocated scientific bytes against the pinned Git
baseline and creates a temporary original-layout view using historical code.
It runs the original seal and saved-context analysis without model/provider calls:

```sh
python -m tools.historical check
python -m tools.historical verify --corpus-dir /absolute/path/to/corpus/combined-v2
python -m tools.evaluation.render_case_index --check
python -m unittest discover -v
```

A full-history clone contains the required baseline and original archive commit.
For a shallow clone, fetch `c8caa0cf1327b73f358ad4c2e3c16c9736d079d9`
from origin first. Verification never fetches automatically. The full replay
needs all ignored pinned PDF/text inputs; the byte check and tests do not.
New code and presentation changes are reviewed/tested separately from this
historical runtime. The original seal and release overlay have not been broadened
or replaced with an exemption for moved scientific files.
