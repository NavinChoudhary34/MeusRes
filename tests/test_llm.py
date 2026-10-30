
from meusres.llm import generate_digest


def test_generate_digest():
    prompt = """
    Explain what artificial intelligence is
    in approximately 100 words.
    """

    digest = generate_digest(prompt)

    assert isinstance(digest, str)
    assert len(digest) > 0

    print("\nGenerated answer:")
    print(digest)
