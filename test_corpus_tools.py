"""Offline protection for corpus duplication guards and evaluation comparisons."""
import contextlib
import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import MagicMock, patch

import httpx

import compare_evals
import ingest_corpus


class CorpusIngestionTests(unittest.TestCase):
    def test_unreachable_or_loading_service_aborts_before_ingestion(self):
        for failure in (httpx.ConnectError("test connection failure"), None):
            client = MagicMock()
            client.get.side_effect = failure
            client.get.return_value = httpx.Response(503, json={"status": "loading"})
            with self.subTest(failure=failure), contextlib.redirect_stdout(io.StringIO()):
                with self.assertRaises(SystemExit) as raised:
                    ingest_corpus.check_existing_chunks(client)
                self.assertEqual(raised.exception.code, 1)

    def test_populated_store_requires_affirmative_answer_before_any_ingest(self):
        with tempfile.TemporaryDirectory() as directory:
            manifest = Path(directory, "manifest.json")
            manifest.write_text(json.dumps({"articles": [{"filename": "test.pdf"}]}))
            Path(directory, "test.pdf").touch()
            for answer, expected in [("", 1), ("no", 1), (" YES ", 0)]:
                with self.subTest(answer=answer), patch("sys.argv", ["ingest_corpus.py", "--manifest", str(manifest),
                                                                       "--corpus-dir", directory]), patch.object(
                    ingest_corpus.httpx, "Client"
                ), patch.object(ingest_corpus, "check_existing_chunks", return_value=7), patch(
                    "builtins.input", return_value=answer
                ), patch.object(ingest_corpus, "ingest_file", return_value=2) as ingest, contextlib.redirect_stdout(io.StringIO()):
                    self.assertEqual(ingest_corpus.main(), expected)
                    if expected:
                        ingest.assert_not_called()
                    else:
                        self.assertEqual(ingest.call_args.args[1], Path(directory, "test.pdf"))
                        self.assertEqual(ingest.call_args.kwargs, {"source": "test.pdf"})

    def test_unreadable_or_textless_pdf_never_posts_to_service(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory, "test.pdf")
            client = MagicMock()
            for failure in (ValueError("test malformed PDF"), None):
                with self.subTest(failure=failure), patch.object(ingest_corpus, "PdfReader", side_effect=failure) as reader, contextlib.redirect_stdout(io.StringIO()):
                    page = MagicMock()
                    page.extract_text.return_value = None
                    reader.return_value.pages = [page]
                    self.assertEqual(ingest_corpus.ingest_file(client, path, "test.pdf"), None if failure else 0)
            client.post.assert_not_called()


class ComparisonTests(unittest.TestCase):
    def test_comparison_reports_both_flip_directions_and_ignores_unanswerable(self):
        with tempfile.TemporaryDirectory() as directory:
            baseline, experiment = Path(directory, "before.json"), Path(directory, "after.json")
            before = [
                {"id": "test-a", "category": "direct_lookup", "n3": {"verdict": "fail"}, "n8": {"verdict": "pass"}},
                {"id": "test-b", "category": "unanswerable", "n3": {"verdict": "not_scored"}, "n8": {"verdict": "not_scored"}},
            ]
            after = [
                {"id": "test-a", "category": "direct_lookup", "n3": {"verdict": "pass"}, "n8": {"verdict": "fail"}},
                {"id": "test-b", "category": "unanswerable", "n3": {"verdict": "pass"}, "n8": {"verdict": "pass"}},
            ]
            baseline.write_text(json.dumps({"results": before}))
            experiment.write_text(json.dumps({"results": after}))
            for path, changed in [(experiment, True), (baseline, False)]:
                output = io.StringIO()
                with self.subTest(changed=changed), patch("sys.argv", ["compare_evals.py", str(baseline), str(path)]), contextlib.redirect_stdout(output):
                    compare_evals.main()
                text = output.getvalue()
                self.assertNotIn("test-b", text)
                if changed:
                    self.assertIn("n=3: 0/1 → 1/1", text)
                    self.assertIn("n=8: 1/1 → 0/1", text)
                    self.assertIn("IMPROVED  test-a", text)
                    self.assertIn("REGRESSED  test-a", text)
                else:
                    self.assertIn("No changes between runs.", text)
