"""Link already acquired corpus files into a temporary regression input view."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
BENCHMARK = ROOT / "benchmark/outliers/v1/regression"
DEST = ROOT / "corpus/outliers-v1/topic-regression"
SOURCES = [
    ROOT / "corpus/cardiology-v1",
    ROOT / "corpus/diabetes-v1",
    ROOT / "corpus/oncology-v1",
    ROOT / "corpus/outliers-v1",
]


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


manifest = json.loads((BENCHMARK / "manifest.json").read_text(encoding="utf-8"))
DEST.mkdir(parents=True, exist_ok=True)
for article in manifest["articles"]:
    for suffix, expected in [(".pdf", article["download"]["pdf_sha256"]),
                             (".txt", article["validation"]["extracted_text_sha256"])]:
        name = Path(article["filename"]).with_suffix(suffix).name
        target = DEST / name
        matches = [folder / name for folder in SOURCES if (folder / name).is_file()]
        matches = [p for p in matches if sha(p) == expected]
        if not matches:
            raise FileNotFoundError(f"No source file matches the pinned hash for {name}")
        if target.exists() or target.is_symlink():
            if not target.is_file() or sha(target) != expected:
                raise FileExistsError(f"Existing regression input differs from the pinned source: {target}")
            continue
        target.symlink_to(matches[0].resolve())

print(f"Prepared {len(manifest['articles'])} article inputs in {DEST}")
