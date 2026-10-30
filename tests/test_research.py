
from meusres.database import Base, engine, SessionLocal
from meusres.models import ResearchRun
from meusres.research import save_research


def test_save_research():

    # Ensure tables exist
    Base.metadata.create_all(bind=engine)

    test_sources = [
        {
            "title": "Python Official Website",
            "url": "https://www.python.org/",
            "snippet": "Python programming language",
            "page_text": "Python is a programming language.",
        },
        {
            "title": "Ollama Website",
            "url": "https://ollama.com/",
            "snippet": "Run local language models",
            "page_text": "Ollama allows running models locally.",
        },
    ]

    research_id = save_research(
        query="Test research query",
        answer="This is a test research answer.",
        model="qwen3.5:0.8b",
        sources=test_sources,
    )

    # Verify the saved record
    db = SessionLocal()

    try:
        research = db.get(ResearchRun, research_id)

        assert research is not None
        assert research.query == "Test research query"
        assert research.answer == "This is a test research answer."
        assert research.model == "qwen3.5:0.8b"
        assert len(research.sources) == 2

        print("\nResearch saved successfully!")
        print("Research ID:", research.id)
        print("Query:", research.query)
        print("Number of sources:", len(research.sources))

    finally:
        # Remove test record so it doesn't pollute your history
        if research_id:
            research = db.get(ResearchRun, research_id)

            if research:
                db.delete(research)
                db.commit()

        db.close()
