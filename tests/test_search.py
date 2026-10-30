
from meusres.search import search_web


def test_search_web():
    results = search_web("Python programming language")

    assert isinstance(results, list)

    print(f"Number of results: {len(results)}")

    if results:
        print("First result:", results[0])
