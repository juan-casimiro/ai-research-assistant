"""Check original experiment bytes and the versioned release presentation overlay.

No corpus, model, provider or network is used. The immutable archive commit must
be available locally; scientific inputs/results are always checked in place.
"""
import hashlib
import json
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[2]
ARCHIVE_COMMIT = "e3eada3363ad7eb7b1f56d5a5053496a24498a8a"
SEAL_PATH = "benchmark/combined/v2/artifact_hashes.json"
VERIFIER_PATH = "benchmark/combined/verify_corrected_release.py"
# Original experiment seal is immutable, even when presentation evolves.
SEAL_SHA256 = "8bfbf05a07d757211b9f353326c58a0b7df2fc6c6bc94ac956ae54debf762074"


def digest(data):
    return hashlib.sha256(data).hexdigest()


def historical_bytes(root, path):
    result = subprocess.run(["git", "show", f"{ARCHIVE_COMMIT}:{path}"],
                            cwd=root, capture_output=True, check=False)
    if result.returncode:
        raise ValueError("archive bytes unavailable; fetch origin tag "
                         "benchmark-epic-before-cleanup-2026-10-06")
    return result.stdout


def verify_artifacts(root=ROOT):
    root = Path(root)
    seal_bytes = (root / SEAL_PATH).read_bytes()
    if digest(seal_bytes) != SEAL_SHA256:
        raise ValueError("original experiment seal changed")
    files = json.loads(seal_bytes)["files"]
    overlay = json.loads((root / "benchmark/combined/v2/release_verification_v1.json").read_text())
    if (overlay["schema_version"] != "1.0" or overlay["archive_commit"] != ARCHIVE_COMMIT or
            overlay["original_seal_sha256"] != SEAL_SHA256):
        raise ValueError("release overlay identity differs")
    transitions = overlay["transitions"]
    for name, transition in transitions.items():
        if name not in files or not (name.endswith(".md") or name == VERIFIER_PATH):
            raise ValueError(f"non-presentation artifact cannot be exempted: {name}")
        expected_kind = "verifier_migration" if name == VERIFIER_PATH else "presentation_documentation"
        if transition["kind"] != expected_kind:
            raise ValueError(f"invalid transition kind: {name}")
        if digest(historical_bytes(root, name)) != files[name]:
            raise ValueError(f"original archive bytes differ: {name}")
    for name, expected in files.items():
        current = transitions[name]["current_sha256"] if name in transitions else expected
        if digest((root / name).read_bytes()) != current:
            raise ValueError(f"artifact drift: {name}")
    # Check added verifier code as well as the transitioned sealed entry point.
    verifier = "benchmark/combined/verify_release_artifacts.py"
    if digest((root / verifier).read_bytes()) != overlay["artifact_verifier_sha256"]:
        raise ValueError("artifact verifier drift")
    print(f"Verified {len(files)} sealed paths; {len(transitions)} explicit release transitions")


if __name__ == "__main__":
    verify_artifacts()
