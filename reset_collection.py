# reset_collection.py
import chromadb

chroma_client = chromadb.PersistentClient(path="./chroma_db")
try:
    chroma_client.delete_collection("documents")
    print("Collection reset.")
except Exception:
    print("No existing collection to reset.")