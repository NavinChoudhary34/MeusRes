
from meusres import pipeline


def test_run_research(monkeypatch):

    # Mock web search
    def mock_search(query):
        return [
            {
                "title": "Test Article",
                "url": "https://example.com/article",
                "content": "Test search snippet",
            }
        ]

    # Mock webpage extraction
    def mock_fetch(url):
        return "This is extracted test webpage content."

    # Mock LLM generation
    def mock_generate(prompt):
        assert "Test research topic" in prompt
        return "This is a generated research digest."

    # Mock database saving
    def mock_save_research(query, answer, model, sources):
        assert query == "Test research topic"
        assert answer == "This is a generated research digest."
        assert len(sources) == 1
        return 123

    monkeypatch.setattr(pipeline, "search_web", mock_search)
    monkeypatch.setattr(pipeline, "fetch_text", mock_fetch)
    monkeypatch.setattr(pipeline, "generate_digest", mock_generate)
    monkeypatch.setattr(pipeline, "save_research", mock_save_research)

    result = pipeline.run_research("Test research topic")

    assert result["research_id"] == 123
    assert result["query"] == "Test research topic"
    assert result["answer"] == "This is a generated research digest."
    assert len(result["sources"]) == 1

    print("\nPipeline test passed!")
    print("Research ID:", result["research_id"])
    print("Answer:", result["answer"])
