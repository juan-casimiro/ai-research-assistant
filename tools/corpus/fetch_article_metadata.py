#!/usr/bin/env python3
"""Fetch corpus article metadata from a pinned PMCID and PubMed.

Eligibility reflects the supported article licence, not figure/table rights. Discovery
queries are caller-supplied provenance; PubMed cannot recover a past search.
"""
import argparse
import copy
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re
import time
from urllib.error import HTTPError
from urllib.parse import parse_qs, urlencode, urlsplit
import xml.etree.ElementTree as ET

from .download_corpus import BUCKET, open_url

ID_CONVERTER = "https://pmc.ncbi.nlm.nih.gov/tools/idconv/api/v1/articles/"
EFETCH = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"


def element_text(element) -> str:
    """Preserve whitespace between nested prose elements and inline markup."""
    if element is None:
        return ""
    return " ".join("".join(element.itertext()).split())


def cloud_url(s3_url: str) -> str:
    prefix = "s3://pmc-oa-opendata/"
    if not isinstance(s3_url, str) or not s3_url.startswith(prefix):
        raise ValueError("metadata contains an unsupported PMC object URL")
    return BUCKET + "/" + s3_url[len(prefix):]


def read_bytes(url: str) -> bytes:
    for attempt in range(4):
        time.sleep(0.4)  # Pace public metadata requests without an API key.
        try:
            with open_url(url) as response:
                return response.read()
        except HTTPError as error:
            if error.code not in {429, 502, 503, 504} or attempt == 3:
                raise
            time.sleep(2 ** (attempt + 1))


def read_pmc_xml(s3_url: str) -> bytes:
    """Check the provider's checksum before using or archiving article XML."""
    data = read_bytes(cloud_url(s3_url))
    checksum = parse_qs(urlsplit(s3_url).query).get("md5", [None])[0]
    if checksum and hashlib.md5(data).hexdigest() != checksum:
        raise ValueError("PMC XML checksum mismatch")
    return data


def author_name(author) -> str:
    """Read structured or prose JATS names without dropping author entries."""
    name_parts = ["prefix", "given-names", "surname", "suffix"]
    for tag in ["name", "string-name", "collab"]:
        name = author.find(tag)
        if name is None:
            continue
        prose_name = tag == "string-name" and (
            (name.text or "").strip()
            or any((child.tail or "").strip() or child.tag not in name_parts for child in name)
        )
        if tag == "collab":
            # Group labels can contain a nested roster; retain inline name markup
            # but exclude member details and reference markers from the label.
            label = copy.deepcopy(name)
            for parent in label.iter():
                for child in list(parent):
                    if child.tag in {"contrib-group", "xref"}:
                        parent.remove(child)
            value = element_text(label)
        elif prose_name:
            value = element_text(name)
        else:
            parts = [element_text(name.find(key)) for key in name_parts]
            value = " ".join(filter(None, parts)) or element_text(name)
        if value:
            return value
    raise ValueError("PMC XML has an author without a supported name")


def licence_eligibility(license_name: str, urls: list[str]) -> str:
    """Accept only explicit, compatible CC BY 4.0/CC0 evidence."""
    parsed = [urlsplit(url) for url in urls]
    if not parsed or any(u.scheme not in {"http", "https"} or u.hostname != "creativecommons.org" for u in parsed):
        return "excluded"
    paths = {u.path for u in parsed}
    by, zero = "/licenses/by/4.0/", "/publicdomain/zero/1.0/"
    if license_name == "CC BY 4.0" and by in paths and paths <= {by, zero}:
        return "eligible"
    if license_name == "CC0 1.0" and paths == {zero}:
        return "eligible"
    return "excluded"


def parse_record(metadata: dict, jats: bytes, pubmed: bytes, identifiers: dict) -> dict:
    """Join identifiers and version-specific PMC metadata with PubMed prose."""
    pmcid, doi, pmid = metadata["pmcid"], metadata["doi"], str(metadata["pmid"])
    mapping = [r for r in identifiers.get("records", []) if r.get("pmcid") == pmcid]
    if len(mapping) != 1 or str(mapping[0].get("pmid")) != pmid or mapping[0].get("doi", "").lower() != doi.lower():
        raise ValueError("PMCID converter disagrees with the pinned PMC DOI/PMID")
    if metadata.get("is_retracted"):
        raise ValueError("pinned PMC record is retracted")
    article = ET.fromstring(jats)
    front = article.find("./front/article-meta")
    if front is None:
        raise ValueError("PMC XML has no article metadata")
    xml_dois = [element_text(e).lower() for e in front.findall("article-id") if e.get("pub-id-type") == "doi"]
    if doi.lower() not in xml_dois:
        raise ValueError("PMC XML DOI disagrees with cloud metadata")
    pubmed_matches = [e for e in ET.fromstring(pubmed).findall("PubmedArticle") if element_text(e.find("./MedlineCitation/PMID")) == pmid]
    if len(pubmed_matches) != 1:
        raise ValueError("requested PMID is missing or duplicated in PubMed response")
    pubmed_article = pubmed_matches[0]
    corrections = pubmed_article.findall("./MedlineCitation/CommentsCorrectionsList/CommentsCorrections")
    if any(e.get("RefType") in {"RetractionIn", "RetractionOf"} for e in corrections):
        raise ValueError("PubMed reports a retraction; review this candidate")
    pubmed_dois = [element_text(e).lower() for e in pubmed_article.findall("./PubmedData/ArticleIdList/ArticleId") if e.get("IdType") == "doi"]
    if doi.lower() not in pubmed_dois:
        raise ValueError("PubMed DOI disagrees with the pinned PMC version")
    citation = pubmed_article.find("./MedlineCitation/Article")
    title = element_text(front.find("./title-group/article-title"))
    normalize = lambda s: re.sub(r"[\W_]", "", s.casefold())
    if normalize(title).rstrip(".") != normalize(element_text(citation.find("ArticleTitle"))).rstrip("."):
        raise ValueError("PubMed and PMC titles disagree; review article identity")
    authors = []
    for author in front.findall("./contrib-group/contrib"):
        if author.get("contrib-type") != "author":
            continue
        authors.append(author_name(author))
    if not authors:
        raise ValueError("PMC XML lacks author metadata")
    dates = front.findall("pub-date")
    chosen = next((d for d in dates if d.get("pub-type") == "epub" or d.get("publication-format") == "electronic" and d.get("date-type") == "pub"), dates[0] if dates else None)
    if chosen is None or not element_text(chosen.find("year")):
        raise ValueError("PMC XML lacks a publication year")
    parts = [element_text(chosen.find(k)) for k in ["year", "month", "day"]]
    precision = "day" if all(parts) else "month" if all(parts[:2]) else "year"
    count = {"day": 3, "month": 2, "year": 1}[precision]
    date = "-".join([parts[0]] + [p.zfill(2) for p in parts[1:count]])
    abstract_sections = [{"label": e.get("Label"), "text": element_text(e)} for e in citation.findall("./Abstract/AbstractText")]
    abstract = "\n\n".join((s["label"] + ": " if s["label"] else "") + s["text"] for s in abstract_sections) or None
    permissions = front.find("permissions")
    notice = element_text(permissions)
    licence_urls = sorted(set(re.findall(r"https?://creativecommons\.org/(?:licenses/[\w-]+/[\d.]+|publicdomain/zero/[\d.]+)/", ET.tostring(permissions, encoding="unicode") if permissions is not None else "")))
    exact_licences = sorted(set(urlsplit(u).path for u in licence_urls))
    by4_and_data = {"/licenses/by/4.0/", "/publicdomain/zero/1.0/"}
    licence = "CC BY 4.0" if "/licenses/by/4.0/" in exact_licences and set(exact_licences) <= by4_and_data else "CC0 1.0" if exact_licences == ["/publicdomain/zero/1.0/"] else metadata.get("license_code")
    return {
        "pmcid": pmcid, "pmc_version": metadata["version"], "pmid": pmid,
        "doi": doi, "title": title, "authors": authors,
        "journal": element_text(article.find("./front/journal-meta/journal-title-group/journal-title")),
        "publication_date": date, "publication_date_precision": precision,
        "year": int(parts[0]), "article_type": article.get("article-type"),
        "abstract": abstract, "abstract_sections": abstract_sections,
        "abstract_absence_reason": None if abstract else "No abstract in the PubMed record",
        "abstract_summary": None, "license": licence, "license_notes": notice,
        "licence_urls": licence_urls,
        "page_count": None, "has_structured_sections": bool(article.findall("./body/sec")),
        "notes": "Article licence status is based on pinned metadata; check PDF identity/readability separately.",
        "pubmed_url": f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/",
        "article_url": f"https://pmc.ncbi.nlm.nih.gov/articles/{pmcid}.{metadata['version']}/",
        "pubmed_title": element_text(citation.find("ArticleTitle")),
        "pubmed_publication_types": [element_text(e) for e in citation.findall("./PublicationTypeList/PublicationType")],
        "pubmed_corrections": [dict(e.attrib, text=element_text(e)) for e in pubmed_article.findall("./MedlineCitation/CommentsCorrectionsList/CommentsCorrections")],
        "pmc_related_articles": [dict(e.attrib, text=element_text(e)) for e in front.findall("related-article")],
        "eligibility": licence_eligibility(licence, licence_urls),
    }


def fetch_metadata(pmcid: str, version: int, search_query: str, filename: str, cluster: str, archive_dir: Path | None = None) -> dict:
    if not re.fullmatch(r"PMC[0-9]+", pmcid) or type(version) is not int or version < 1:
        raise ValueError("use a valid PMCID and explicitly chosen positive deposit version")
    if not search_query.strip() or not cluster.strip():
        raise ValueError("supply discovery query and topic cluster")
    if not re.fullmatch(re.escape(pmcid) + r"-[a-z0-9]+(?:-[a-z0-9]+){0,6}\.pdf", filename):
        raise ValueError("filename must be PMCID followed by 1–7 lowercase hyphen-separated words and .pdf")
    metadata_url = f"{BUCKET}/metadata/{pmcid}.{version}.json"
    raw_metadata = read_bytes(metadata_url)
    metadata = json.loads(raw_metadata)
    if metadata.get("pmcid") != pmcid or metadata.get("version") != version:
        raise ValueError("cloud response does not match requested PMCID/version")
    if not metadata.get("pmid"):
        raise ValueError("this PMCID has no PMID; PubMed metadata is unavailable")
    converter_url = ID_CONVERTER + "?" + urlencode({"ids": pmcid, "format": "json", "versions": "yes", "tool": "ai-research-assistant"})
    pubmed_url = EFETCH + "?" + urlencode({"db": "pubmed", "id": metadata["pmid"], "retmode": "xml", "tool": "ai-research-assistant"})
    sources = {"cloud.json": (metadata_url, raw_metadata), "id-converter.json": (converter_url, read_bytes(converter_url)), "pubmed.xml": (pubmed_url, read_bytes(pubmed_url)), "article.xml": (cloud_url(metadata["xml_url"]), read_pmc_xml(metadata["xml_url"]))}
    result = parse_record(metadata, sources["article.xml"][1], sources["pubmed.xml"][1], json.loads(sources["id-converter.json"][1]))
    # Preserve the metadata helper's article_id alias alongside the canonical id.
    article_id = filename[:-4]
    result.update(id=article_id, article_id=article_id,
                  filename=filename, cluster=cluster, search_query=search_query,
                  metadata_fetched_at=datetime.now(timezone.utc).isoformat())
    result["metadata_url"] = metadata_url
    result["metadata_sha256"] = hashlib.sha256(raw_metadata).hexdigest()
    result["metadata_sources"] = {name: {"url": url, "sha256": hashlib.sha256(data).hexdigest()} for name, (url, data) in sources.items()}
    if archive_dir is not None:
        archive_dir.mkdir(parents=True, exist_ok=True)
        for name, (_, data) in sources.items():
            (archive_dir / f"{pmcid}.{version}.{name}").write_bytes(data)
    return result


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--pmcid", required=True)
    parser.add_argument("--pmc-version", type=int, required=True)
    parser.add_argument("--search-query", required=True)
    parser.add_argument("--filename", required=True,
                        help="PMCID-brief-title-summary.pdf; 1–7 lowercase hyphen-separated words after PMCID")
    parser.add_argument("--cluster", required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--archive-dir", type=Path)
    args = parser.parse_args(argv)
    try:
        record = fetch_metadata(args.pmcid, args.pmc_version, args.search_query, args.filename, args.cluster, args.archive_dir)
        args.output.write_text(json.dumps(record, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    except (OSError, ValueError, KeyError, TypeError, ET.ParseError) as error:
        print(f"ERROR: {error}")
        return 1
    print(f"Metadata saved: {args.pmcid} -> PMID {record['pmid']}; eligibility={record['eligibility']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
