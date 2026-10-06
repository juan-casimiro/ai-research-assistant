"""Offline release-overlay checks: documentation transitions never exempt evidence."""
import hashlib
import json
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch

from benchmark.combined import verify_release_artifacts as verifier


class ReleaseArtifactTests(unittest.TestCase):
    def setUp(self):
        self.temporary = TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.files = {"README.md": b"synthetic original documentation",
                      "benchmark/synthetic/queries.json": b'{"question":"synthetic frozen question"}'}
        for name, content in self.files.items():
            self.write(name, content)
        self.write("README.md", b"synthetic release documentation")
        self.write("benchmark/combined/verify_release_artifacts.py", b"synthetic verifier code")
        seal = json.dumps({"files": {name: verifier.digest(data) for name, data in self.files.items()}}).encode()
        self.write(verifier.SEAL_PATH, seal)
        self.seal_hash = verifier.digest(seal)
        self.overlay = {"schema_version": "1.0", "archive_commit": verifier.ARCHIVE_COMMIT,
                        "original_seal_sha256": self.seal_hash,
                        "artifact_verifier_sha256": verifier.digest(b"synthetic verifier code"),
                        "transitions": {"README.md": {"kind": "presentation_documentation",
                            "current_sha256": verifier.digest(b"synthetic release documentation")}}}

    def write(self, name, data):
        path = self.root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)

    def verify(self, history=None):
        self.write("benchmark/combined/v2/release_verification_v1.json", json.dumps(self.overlay).encode())
        with patch.object(verifier, "SEAL_SHA256", self.seal_hash), patch.object(
                verifier, "historical_bytes", side_effect=lambda root, name: (history or self.files)[name]):
            verifier.verify_artifacts(self.root)

    def test_release_documentation_uses_verified_original_archive_bytes(self):
        self.verify()

    def test_changed_scientific_input_is_rejected(self):
        self.write("benchmark/synthetic/queries.json", b"synthetic improved gold")
        with self.assertRaisesRegex(ValueError, "artifact drift"):
            self.verify()

    def test_overlay_cannot_exempt_scientific_input(self):
        self.overlay["transitions"]["benchmark/synthetic/queries.json"] = {
            "kind": "presentation_documentation", "current_sha256": verifier.digest(b"synthetic changed gold")}
        with self.assertRaisesRegex(ValueError, "cannot be exempted"):
            self.verify()

    def test_wrong_historical_documentation_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "archive bytes differ"):
            self.verify({"README.md": b"synthetic fabricated history"})

    def test_unrecorded_documentation_drift_is_rejected(self):
        self.write("README.md", b"synthetic unrecorded release edit")
        with self.assertRaisesRegex(ValueError, "artifact drift"):
            self.verify()

    def test_rewritten_original_seal_is_rejected(self):
        self.write(verifier.SEAL_PATH, b'{"files":{}}')
        with self.assertRaisesRegex(ValueError, "original experiment seal changed"):
            self.verify()

    def test_added_verifier_code_drift_is_rejected(self):
        self.write("benchmark/combined/verify_release_artifacts.py", b"synthetic altered verifier")
        with self.assertRaisesRegex(ValueError, "verifier drift"):
            self.verify()
