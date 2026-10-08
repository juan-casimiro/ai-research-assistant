"""The production PDF extraction method, shared with corpus preparation."""
from pypdf import PdfReader

METHOD = 'pypdf.PdfReader(str(pdf_path)); page.extract_text() or ""; newline join; UTF-8'


def extract_pages(reader):
    return [page.extract_text() or "" for page in reader.pages]


def extract_pdf(pdf_path):
    pages = extract_pages(PdfReader(str(pdf_path)))
    return "\n".join(pages), [i for i, text in enumerate(pages, 1) if not text.strip()]
