
from sqlalchemy.orm import Session

from meusres.database import SessionLocal
from meusres.models import ResearchRun, Source


def save_research(
    query: str,
    answer: str,
    model: str,
    sources: list[dict],
) -> int:
    """
    Save a completed research run and its sources.
    Returns the ID of the saved research run.
    """

    db: Session = SessionLocal()

    try:
        research = ResearchRun(
            query=query,
            answer=answer,
            model=model,
            status="completed",
        )

        # Attach the sources to this research run
        for item in sources:
            url = item.get("url")

            if not url:
                continue

            source = Source(
                title=item.get("title") or None,
                url=url,
                snippet=item.get("snippet") or None,
                extracted_text=item.get("page_text") or None,
            )

            research.sources.append(source)

        db.add(research)
        db.commit()

        # Get the generated database ID
        db.refresh(research)

        return research.id

    except Exception:
        db.rollback()
        raise

    finally:
        db.close()
