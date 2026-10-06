"""Verify and replay frozen experiments with their original paths and source code.

The temporary tree uses the pinned pre-move Git commit for the runtime, and
verified relocated files for scientific inputs/results. It never modifies the
checkout or weakens the original experiment seal. Active tools have new source
fingerprints; this runner explicitly reproduces the historical runtime instead.
"""
import argparse
from contextlib import contextmanager
import hashlib
import io
import json
from pathlib import Path
import subprocess
import sys
import tarfile
from tempfile import TemporaryDirectory

ROOT = Path(__file__).resolve().parents[1]
SOURCE_COMMIT = "c8caa0cf1327b73f358ad4c2e3c16c9736d079d9"
HISTORICAL_TESTS = (
    "test_combined_baseline", "test_corrected_combined",
    "test_release_artifacts", "test_isolated_ingestion",
)


def digest(data):
    return hashlib.sha256(data).hexdigest()


@contextmanager
def original_layout(root=ROOT):
    """Build a checked original-layout view; remove it after the caller finishes."""
    root = Path(root)
    layout = json.loads((root / "data/layout.json").read_text())
    if layout["source_commit"] != SOURCE_COMMIT:
        raise ValueError("layout source commit differs from the pinned migration baseline")
    result = subprocess.run(
        ["git", "archive", "--format=tar", SOURCE_COMMIT], cwd=root,
        capture_output=True, check=False,
    )
    if result.returncode:
        raise ValueError(f"migration baseline unavailable; fetch origin commit {SOURCE_COMMIT}")
    with TemporaryDirectory(prefix="ara-historical-") as temporary:
        view = Path(temporary)
        with tarfile.open(fileobj=io.BytesIO(result.stdout)) as archive:
            original_files = [member.name for member in archive.getmembers()
                              if member.isfile() or member.issym()]
            archive.extractall(view, filter="data")
        for name in original_files:
            if not (root / name).exists() and name not in layout["moves"]:
                raise ValueError(f"missing relocation record: {name}")
        immutable = 0
        destinations = set()
        for old, entry in layout["moves"].items():
            original = view / old
            current = root / entry["path"]
            if (Path(old).is_absolute() or ".." in Path(old).parts or
                    Path(entry["path"]).is_absolute() or ".." in Path(entry["path"]).parts or
                    entry["path"] in destinations):
                raise ValueError(f"invalid relocation: {old}")
            destinations.add(entry["path"])
            if digest(original.read_bytes()) != entry["sha256"]:
                raise ValueError(f"relocation inventory differs from Git baseline: {old}")
            target = str(original.readlink()) if original.is_symlink() else None
            if target != entry["symlink_target"]:
                raise ValueError(f"original link inventory differs: {old}")
            # Documentation and active utilities may be adapted. Frozen data,
            # archived helpers and archived regression tests remain exact bytes.
            preserved = (original.suffix not in (".md", ".py") or
                         entry["path"].startswith("tools/evaluation/historical/"))
            if preserved:
                content = current.read_bytes()
                if digest(content) != entry["sha256"]:
                    raise ValueError(f"relocated artifact drift: {entry['path']}")
                if not original.is_symlink():
                    original.write_bytes(content)
                immutable += 1
        # Original seal checks read historical Git objects; no checkout writes.
        git_directory = subprocess.run(
            ["git", "rev-parse", "--absolute-git-dir"], cwd=root,
            capture_output=True, text=True, check=True,
        ).stdout.strip()
        (view / ".git").write_text(f"gitdir: {git_directory}\n")
        print(f"Verified {immutable} relocated immutable artifacts against {SOURCE_COMMIT}", flush=True)
        yield view


def run_tests(root=ROOT):
    with original_layout(root) as view:
        subprocess.run([sys.executable, "-m", "unittest", "-v", *HISTORICAL_TESTS],
                       cwd=view, check=True)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("check", help="Check immutable relocated bytes against Git")
    commands.add_parser("test", help="Run the preserved historical helper regressions")
    verify = commands.add_parser("verify", help="Replay the sealed saved release offline")
    verify.add_argument("--corpus-dir", type=Path, required=True)
    script = commands.add_parser("script", help="Run an archived helper in its original layout")
    script.add_argument("path", help="Original repository path, for example benchmark/combined/build_release.py")
    script.add_argument("arguments", nargs=argparse.REMAINDER)
    args = parser.parse_args(argv)
    if args.command == "test":
        run_tests()
        return
    with original_layout() as view:
        if args.command == "verify":
            subprocess.run([sys.executable, "benchmark/combined/verify_corrected_release.py",
                            "--corpus-dir", str(args.corpus_dir.resolve())], cwd=view, check=True)
        elif args.command == "script":
            moves = json.loads((ROOT / "data/layout.json").read_text())["moves"]
            entry = moves.get(args.path, {})
            if not entry.get("path", "").startswith("tools/evaluation/historical/") or not args.path.endswith(".py"):
                parser.error("script must name an archived helper from data/layout.json")
            subprocess.run([sys.executable, args.path, *args.arguments], cwd=view, check=True)


if __name__ == "__main__":
    main()
