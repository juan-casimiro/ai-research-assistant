# reset_collection.py
import os

import chromadb
from dotenv import load_dotenv

load_dotenv()

CHROMA_PATH = os.getenv("CHROMA_PATH", "./chroma_db")

chroma_client = chromadb.PersistentClient(path=CHROMA_PATH)
try:
    chroma_client.delete_collection("documents")
    print(f"Collection reset ({CHROMA_PATH}).")
except Exception:
    print(f"No existing collection to reset ({CHROMA_PATH}).")