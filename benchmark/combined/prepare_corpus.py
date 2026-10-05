"""Prepare a local input view from already acquired, checksum-pinned topic files."""
import argparse
import hashlib
import json
from pathlib import Path


def prepare(release, corpus_dir, sources):
    manifest = json.loads((release / "manifest.json").read_text())
    corpus_dir.mkdir(parents=True, exist_ok=True)
    for article in manifest["articles"]:
        for suffix, expected in [(".pdf", article["download"]["pdf_sha256"]),
                                 (".txt", article["validation"]["extracted_text_sha256"])]:
            name = Path(article["filename"]).with_suffix(suffix).name
            matches = [directory / name for directory in sources if (directory / name).is_file()]
            source = next((p for p in matches if hashlib.sha256(p.read_bytes()).hexdigest() == expected), None)
            if source is None:
                raise ValueError(f"no pinned source file: {name}")
            destination = corpus_dir / name
            if destination.exists() or destination.is_symlink():
                if not destination.is_file() or hashlib.sha256(destination.read_bytes()).hexdigest() != expected:
                    raise ValueError(f"existing corpus view differs: {name}")
            else:
                destination.symlink_to(source.resolve())
    print(f"Verified and prepared {len(manifest['articles'])} local PDF/text pairs")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--benchmark", type=Path, required=True)
    parser.add_argument("--corpus-dir", type=Path, required=True)
    parser.add_argument("--sources", nargs="+", type=Path, required=True)
    args = parser.parse_args()
    prepare(args.benchmark, args.corpus_dir, args.sources)
