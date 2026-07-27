from fastembed import TextEmbedding
import chromadb

model = TextEmbedding()  # defaults to BAAI/bge-small-en-v1.5
chroma_client = chromadb.PersistentClient(path="./chroma_db")
try:
    chroma_client.delete_collection("test_docs")  # clear any stale data from prior runs
    print("reseting collection..")
except:
    print("no collection to reset on first run")

collection = chroma_client.get_or_create_collection("test_docs")


def embed(text: str) -> list[float]:
    return list(model.embed([text]))[0].tolist()


def embed_query(text: str) -> list[float]:
    prefixed = f"Represent this sentence for searching relevant passages: {text}"
    return list(model.embed([prefixed]))[0].tolist()


if __name__ == "__main__":
    documents = [
        # Strong, unambiguous pet signal
        "She adopted a kitten from the local animal shelter.",
        "My dog loves playing fetch in the park every morning.",
        "The veterinarian gave my puppy his first vaccination today.",
        "We bought a new scratching post for our cat.",
        "Golden retrievers are known for being great family pets.",
        # Weak / single-word pet signal, buried in unrelated context
        "The cat sat on the mat in the sunny living room.",
        "There was a dog barking somewhere in the distance last night.",
        "The house had a small garden and an old cat flap in the door.",
        # Animal-related, but not pets
        "Lions in the wild hunt in coordinated groups called prides.",
        "The migration patterns of humpback whales span thousands of miles.",
        "Bees play a critical role in pollinating crops worldwide.",
        # Tech / ML cluster
        "Machine learning models can classify images with high accuracy.",
        "Neural networks are inspired by biological brain structures.",
        "The transformer architecture revolutionized natural language processing.",
        "Gradient descent is used to optimize model parameters during training.",
        # Completely unrelated
        "The stock market experienced significant volatility this quarter.",
        "Renaissance art often depicted religious and mythological themes.",
        "The recipe calls for two cups of flour and a teaspoon of salt.",
        "Mount Everest is the tallest mountain above sea level.",
        "The committee will vote on the new zoning proposal next week.",
    ]

    embeddings = [embed(doc) for doc in documents]

    collection.add(
        ids=[f"doc_{i}" for i in range(len(documents))],
        embeddings=embeddings,
        documents=documents,
    )

    query = "Tell me about pets"
    query_embedding = embed_query(query)

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=20,  # show the full ranking, all documents
    )

    print("Query:", query)
    print("All matches, ranked:")
    for doc, distance in zip(results["documents"][0], results["distances"][0]):
        print(f"  ({distance:.4f}) {doc}")
