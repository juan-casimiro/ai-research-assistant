"""Offline checks for fresh manifest assembly and preservation on failure."""
import contextlib
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

    def run_builder(self, articles, fetch_error=None, existing=False):
        with tempfile.TemporaryDirectory() as directory:
            candidates, output = Path(directory, "candidates.json"), Path(directory, "manifest.json")
            candidates.write_text(json.dumps({"articles": articles}))
            if existing:
                output.write_text("existing scientific bytes")
            with patch.object(builder, "fetch_metadata", return_value={"title": "Synthetic study", "license": "CC BY 4.0", "licence_urls": ["https://creativecommons.org/licenses/by/4.0/"]},
                              side_effect=fetch_error) as fetch, contextlib.redirect_stdout(io.StringIO()):
                status = builder.main(["--candidates", str(candidates), "--output", str(output)])
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
            with patch.object(builder, "fetch_metadata", return_value=unsupported), contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(builder.main(["--candidates", str(candidates), "--output", str(output)]), 1)
            self.assertFalse(output.exists())
