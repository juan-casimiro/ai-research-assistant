from main import retrieve

# eval_retrieval.py — replace test_cases
test_cases = [
    {
        "query": "What did the University of Minnesota Law School study find about ChatGPT?",
        "expected_keywords": ["Minnesota", "C+"],
    },
    {
        "query": "What privacy concerns exist with ChatGPT?",
        "expected_keywords": ["privacy", "data"],
    },
    {
        "query": "What percentile did ChatGPT score in economics tests?",
        "expected_keywords": ["percentile", "economics"],
    },
    {
        "query": "How does ChatGPT perform on medical licensing exams?",
        "expected_keywords": ["medical", "licensing"],
    },
    {
        "query": "What are the copyright concerns with training data?",
        "expected_keywords": ["copyright", "training data"],
    },
    {
        "query": "How can generative AI help students with disabilities?",
        "expected_keywords": ["disabilities", "neurodivergent"],
    },
    {
        "query": "What did the survey of university students find about ChatGPT usage?",
        "expected_keywords": ["survey", "students"],
    },
    {
        "query": "What bias issues has ChatGPT been criticized for?",
        "expected_keywords": ["bias", "political"],
    },
]

from main import retrieve


def evaluate(n_results: int = 3) -> None:
    hits = 0
    for case in test_cases:
        retrieved_chunks, _ = retrieve(case["query"], n_results)
        retrieved_text = " ".join(retrieved_chunks).lower()

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
