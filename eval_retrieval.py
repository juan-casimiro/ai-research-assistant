from main import embed, collection

# eval_retrieval.py — replace test_cases
test_cases = [
    {
        "query": "How many people globally are estimated to be on the autism spectrum?",
        "expected_keywords": ["127", "61.8 million"],
    },
    {
        "query": "What was the diagnostic delay found in the Nigerian paediatric clinic study?",
        "expected_keywords": ["Nigerian", "44.7"],
    },
    {
        "query": "What were the results of the socially assistive robot therapy trial?",
        "expected_keywords": ["robot", "69"],
    },
    {
        "query": "What is federated learning and why is it relevant to autism AI research?",
        "expected_keywords": ["federated learning", "privacy"],
    },
    {
        "query": "What barriers affect digital health adoption in China according to the survey?",
        "expected_keywords": ["cost", "China"],
    },
]


def evaluate(n_results: int = 3) -> None:
    hits = 0
    for case in test_cases:
        query_embedding = embed(case["query"])
        results = collection.query(
            query_embeddings=[query_embedding], n_results=n_results
        )
        retrieved_text = " ".join(results["documents"][0]).lower()

        found = all(kw.lower() in retrieved_text for kw in case["expected_keywords"])
        status = "✓ HIT " if found else "✗ MISS"
        hits += found
        print(f"{status} {case['query']}")

    accuracy = hits / len(test_cases) * 100
    print(
        f"\nRetrieval accuracy @ n_results={n_results}: {hits}/{len(test_cases)} ({accuracy:.0f}%)"
    )


if __name__ == "__main__":
    evaluate(n_results=3)
    evaluate(n_results=8)
