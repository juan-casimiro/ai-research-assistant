# load_test_pdf.py
import httpx
from pypdf import PdfReader

reader = PdfReader("/Users/juancasimiro/Downloads/ai2.pdf")
text = "\n".join(page.extract_text() or "" for page in reader.pages)

response = httpx.post(
    "http://localhost:8000/ingest",
    json={"text": text, "source": "ai-in-education"},
)
print(response.json())
