"""Keep the byte-preserved historical helper regressions in offline discovery."""
import unittest
import hashlib
import json
from pathlib import Path
import shutil
from tempfile import TemporaryDirectory

from tools.historical import ROOT, original_layout, run_tests


class HistoricalToolsTests(unittest.TestCase):
    def test_preserved_helper_regressions(self):
        run_tests()

    def checkout_copy(self, directory):
        root = Path(directory) / "checkout"
        shutil.copytree(ROOT, root, ignore=shutil.ignore_patterns(".git", "__pycache__", ".venv"))
        (root / ".git").symlink_to(ROOT / ".git")
        return root

    def test_changed_frozen_input_cannot_be_hidden_by_updating_inventory_hash(self):
        with TemporaryDirectory() as directory:
            root = self.checkout_copy(directory)
            manifest = root / "data/archive/v1/corpus_manifest.json"
            manifest.write_text('{"articles": []}\n')
            layout_path = root / "data/layout.json"
            layout = json.loads(layout_path.read_text())
            layout["moves"]["corpus_manifest.json"]["sha256"] = hashlib.sha256(manifest.read_bytes()).hexdigest()
            layout_path.write_text(json.dumps(layout))
            with self.assertRaisesRegex(ValueError, "inventory differs from Git baseline"):
                with original_layout(root):
                    self.fail("changed scientific input was accepted")

    def test_omitted_move_cannot_fall_back_to_old_git_bytes(self):
        with TemporaryDirectory() as directory:
            root = self.checkout_copy(directory)
            layout_path = root / "data/layout.json"
            layout = json.loads(layout_path.read_text())
            del layout["moves"]["corpus_manifest.json"]
            layout_path.write_text(json.dumps(layout))
            with self.assertRaisesRegex(ValueError, "missing relocation record: corpus_manifest.json"):
                with original_layout(root):
                    self.fail("omitted migration was accepted")
