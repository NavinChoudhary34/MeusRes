
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select

from meusres.database import SessionLocal
from meusres.models import ResearchRun
from meusres.pipeline import run_research
from meusres.schemas import ResearchRequest, ResearchResponse


app = FastAPI(
    title="MeusRes API",
    description="Personal AI Research Assistant",
    version="1.0.0",
)


# Database session dependency
def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


@app.get("/")
def home():
    return {
        "message": "Welcome to MeusRes API",
        "status": "running",
    }


# Start a new research run
@app.post("/research", response_model=ResearchResponse)
def create_research(
    request: ResearchRequest,
    db: Session = Depends(get_db),
):
    query = request.query.strip()

    if not query:
        raise HTTPException(
            status_code=400,
            detail="Research query cannot be empty.",
        )

    try:
        result = run_research(query)

        # Retrieve the saved record, including its sources
        research = db.get(ResearchRun, result["research_id"])

        if research is None:
            raise HTTPException(
                status_code=500,
                detail="Research was generated but could not be retrieved.",
            )

        return research

    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Research failed: {str(e)}",
        )


# Retrieve research history
@app.get("/research", response_model=list[ResearchResponse])
def get_research_history(db: Session = Depends(get_db)):

    statement = (
        select(ResearchRun)
        .order_by(ResearchRun.created_at.desc())
    )

    research_runs = db.scalars(statement).all()

    return research_runs


# Retrieve one research run
@app.get("/research/{research_id}", response_model=ResearchResponse)
def get_research(
    research_id: int,
    db: Session = Depends(get_db),
):

    research = db.get(ResearchRun, research_id)

    if research is None:
        raise HTTPException(
            status_code=404,
            detail="Research record not found.",
        )

    return research
