
from meusres.pipeline import run_research


if __name__ == "__main__":
    query = input("Enter your research topic: ").strip()

    try:
        result = run_research(query)

        print("\n" + "=" * 50)
        print("RESEARCH DIGEST")
        print("=" * 50)

        print(result["answer"])

        print("\nResearch ID:", result["research_id"])
        print("Sources:", len(result["sources"]))

    except Exception as e:
        print(f"\nResearch failed: {e}")
