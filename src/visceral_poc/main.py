from enum import Enum
from pydantic import BaseModel, Field
from prometheus_fastapi_instrumentator import Instrumentator
from src.flows.title import generate_titles
from src.flows.tag import generate_tags

from fastapi import FastAPI

app = FastAPI()
Instrumentator().instrument(app).expose(app=app, endpoint="/metrics")


class AgeRatingsEnum(str, Enum):
    AR_3 = "Everyone / 3"
    AR_12 = "Teen / 12"
    AR_16 = "Mature / 16"
    AR_18 = "Adults Only / 18"


class GenerateTitlePayload(BaseModel):
    age_rating: str = Field(..., description="Age rating")
    description: str = Field(..., description="Game description")
    genre: str = Field(..., description="Game genre")
    max_title_length: int = Field(..., description="Maximum length of the title")
    max_word_length: int = Field(
        ..., description="Maximum length of the word in the title"
    )


class GenerateTagPayload(BaseModel):
    age_rating: str = Field(..., description="Age rating")
    description: str = Field(..., description="Game description")
    title: str = Field(..., description="Comma separated titles")
    genre: str = Field(..., description="Game genre")


@app.post("/api/tags")
def read_root(payload: GenerateTagPayload):
    return generate_tags(dict(payload))


@app.post("/api/title")
def read_root(payload: GenerateTitlePayload):
    return generate_titles(dict(payload))

@app.get("/health")
def health_check():
    return {"status": "OK"}
