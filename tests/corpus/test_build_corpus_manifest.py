"""Offline checks for fresh manifest assembly and preservation on failure."""
import contextlib
import hashlib
import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from tools.corpus import build_corpus_manifest as builder


class ManifestTests(unittest.TestCase):
    def candidate(self):
        return dict(pmcid="PMC123456", pmc_version=2, filename="PMC123456-synthetic-study.pdf",
                    cluster="test-topic", search_query="some discovery query")

    def run_builder(self, articles, fetch_error=None, existing=False, missing_pages=None):
        with tempfile.TemporaryDirectory() as directory:
            candidates, output = Path(directory, "candidates.json"), Path(directory, "manifest.json")
            candidates.write_text(json.dumps({"articles": articles}))
            if existing:
                output.write_text("existing scientific bytes")
            with patch.object(builder, "unreadable_pages", return_value=missing_pages or []), patch.object(builder, "fetch_metadata", return_value={"title": "Synthetic study", "license": "CC BY 4.0", "licence_urls": ["https://creativecommons.org/licenses/by/4.0/"]},
                              side_effect=fetch_error) as fetch, contextlib.redirect_stdout(io.StringIO()):
                status = builder.main(["--candidates", str(candidates), "--corpus-dir", directory, "--output", str(output)])
            return status, output.read_text() if output.exists() else None, fetch.call_count

    def test_builds_downloader_compatible_envelope(self):
        status, content, calls = self.run_builder([self.candidate()])
        self.assertEqual(status, 0)
        self.assertEqual(json.loads(content), {"articles": [{"title": "Synthetic study", "license": "CC BY 4.0", "licence_urls": ["https://creativecommons.org/licenses/by/4.0/"], "eligibility": "eligible"}]})
        self.assertEqual(calls, 1)

    def test_invalid_or_duplicate_candidates_fail_before_network(self):
        for articles in [[], [self.candidate(), self.candidate()], [dict(self.candidate(), filename="../test.pdf")],
                         [dict(self.candidate(), pmc_version=True)], [dict(self.candidate(), cluster="")]]:
            with self.subTest(articles=articles):
                self.assertEqual(self.run_builder(articles), (1, None, 0))

    def test_existing_manifest_is_preserved_without_fetching(self):
        self.assertEqual(self.run_builder([self.candidate()], existing=True),
                         (1, "existing scientific bytes", 0))

    def test_failed_metadata_fetch_does_not_publish_partial_manifest(self):
        self.assertEqual(self.run_builder([self.candidate()], ValueError("test identity mismatch")), (1, None, 1))

    def test_unsupported_licence_is_excluded_even_with_claimed_eligibility(self):
        with tempfile.TemporaryDirectory() as directory:
            candidates, output = Path(directory, "candidates.json"), Path(directory, "manifest.json")
            candidates.write_text(json.dumps({"articles": [self.candidate()]}))
            unsupported = {"license": "CC BY 4.0", "licence_urls": [], "eligibility": "eligible"}
            with patch.object(builder, "unreadable_pages", return_value=[]), patch.object(builder, "fetch_metadata", return_value=unsupported), contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(builder.main(["--candidates", str(candidates), "--corpus-dir", directory, "--output", str(output)]), 1)
            self.assertFalse(output.exists())

    def test_pages_without_text_exclude_otherwise_licensed_article(self):
        self.assertEqual(self.run_builder([self.candidate()], missing_pages=[2]), (1, None, 1))

    def test_readability_parser_failure_excludes_article(self):
        with patch.object(builder, "unreadable_pages", side_effect=ValueError("broken PDF")):
            # Exercise the builder directly; run_builder normally supplies its own mock.
            with tempfile.TemporaryDirectory() as directory:
                candidates, output = Path(directory, "candidates.json"), Path(directory, "manifest.json")
                candidates.write_text(json.dumps({"articles": [self.candidate()]}))
                record = {"license": "CC BY 4.0", "licence_urls": ["https://creativecommons.org/licenses/by/4.0/"]}
                with patch.object(builder, "fetch_metadata", return_value=record), contextlib.redirect_stdout(io.StringIO()):
                    self.assertEqual(builder.main(["--candidates", str(candidates), "--corpus-dir", directory, "--output", str(output)]), 1)
                self.assertFalse(output.exists())

    def test_exception_requires_exact_identity_version_hash_and_pages(self):
        payload = b"synthetic exception PDF bytes"
        approved_hash = hashlib.sha256(payload).hexdigest()
        for pmcid, version, checksum, pages, expected in [
            ("PMC12003177", 1, approved_hash, [22, 23, 24], 0),
            ("PMC12003177", 2, approved_hash, [22, 23, 24], 1),
            ("PMC12003177", 1, "wrong-hash", [22, 23, 24], 1),
            ("PMC12003177", 1, approved_hash, [21, 22, 23, 24], 1),
            ("PMC123456", 1, approved_hash, [22, 23, 24], 1),
        ]:
            with self.subTest(pmcid=pmcid, version=version, checksum=checksum, pages=pages), tempfile.TemporaryDirectory() as directory:
                candidate = dict(self.candidate(), pmcid=pmcid, pmc_version=version, filename=pmcid + "-synthetic-study.pdf")
                candidates, output = Path(directory, "candidates.json"), Path(directory, "manifest.json")
                candidates.write_text(json.dumps({"articles": [candidate]}))
                Path(directory, candidate["filename"]).write_bytes(payload)
                record = {"license": "CC BY 4.0", "licence_urls": ["https://creativecommons.org/licenses/by/4.0/"]}
                with patch.object(builder, "READABILITY_EXCEPTION", ("PMC12003177", 1, checksum)), patch.object(builder, "unreadable_pages", return_value=pages), patch.object(builder, "fetch_metadata", return_value=record), contextlib.redirect_stdout(io.StringIO()):
                    status = builder.main(["--candidates", str(candidates), "--corpus-dir", directory, "--output", str(output)])
                self.assertEqual(status, expected)
                self.assertEqual(output.exists(), expected == 0)
                if expected == 0:
                    self.assertIn("User-approved readability exception", json.loads(output.read_text())["articles"][0]["notes"])
