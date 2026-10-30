
from datetime import datetime

from pydantic import BaseModel, ConfigDict


class ResearchRequest(BaseModel):
    query: str


class SourceResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str | None
    url: str
    snippet: str | None
    extracted_text: str | None


class ResearchResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    query: str
    answer: str | None
    model: str
    status: str
    created_at: datetime
    sources: list[SourceResponse] = []
