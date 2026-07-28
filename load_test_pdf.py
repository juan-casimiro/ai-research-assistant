# load_test_pdf.py
import httpx
from pypdf import PdfReader

reader = PdfReader("/Users/juancasimiro/Downloads/ai4.pdf")
text = "\n".join(page.extract_text() or "" for page in reader.pages)

response = httpx.post(
    "http://localhost:8000/ingest",
    json={"text": text, "source": "ai public health"},
)
print(response.json())
# add this to load_test_pdf.py, right after extracting text
print(f"Extracted text length: {len(text)} characters")
print(f"First 500 chars:\n{text[:500]}")
