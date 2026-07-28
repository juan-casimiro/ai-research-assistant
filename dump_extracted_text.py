# dump_extracted_text.py
from pypdf import PdfReader

reader = PdfReader("/Users/juancasimiro/Downloads/ai2.pdf")
text = "\n".join(page.extract_text() or "" for page in reader.pages)

with open("extracted_text.txt", "w", encoding="utf-8") as f:
    f.write(text)

print(f"Wrote {len(text)} characters to extracted_text.txt")
