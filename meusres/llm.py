
import ollama

from meusres.config import MODEL


def generate_digest(prompt: str) -> str:
    """
    Generate a research digest using the local Ollama model.
    """

    print("\nGenerating research digest...")

    response = ollama.chat(
        model=MODEL,
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        think=False,
        options={
            "temperature": 0.2,
            "num_predict": 2048,
        },
    )

    # Extract generated answer
    digest = (response.message.content or "").strip()

    # Debug information
    print("\n--- LLM DEBUG ---")
    print("Model:", response.model)
    print("Response content length:", len(digest))
    print(
        "Thinking output length:",
        len(response.message.thinking or ""),
    )

    # Check whether the model generated an answer
    if not digest:
        print("\nLLM returned empty content.")
        print("Raw response:", response.model_dump_json(indent=2))
        raise ValueError("Ollama returned an empty response.")

    print("\nDigest generated successfully.")

    return digest
