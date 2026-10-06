from main import bm25_documents

for word in ["political", "neurodivergent"]:
    print(f"\n--- Chunks containing '{word}' ---")
    for i, doc in enumerate(bm25_documents):
        if word in doc.lower():
            print(f"  Chunk {i}: {doc[:200]}...")