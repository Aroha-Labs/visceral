from enum import Enum
from pydantic import BaseModel, Field
from flows.title import generate_titles
from flows.tag import generate_tags

from fastapi import FastAPI

app = FastAPI()


class AgeRatingsEnum(str, Enum):
    AR_3 = "Everyone / 3"
    AR_12 = "Teen / 12"
    AR_16 = "Mature / 16"
    AR_18 = "Adults Only / 18"


class GenerateTitlePayload(BaseModel):
    age_rating: str = Field(..., description="Age rating")
    description: str = Field(..., description="Game description")
    tags: str = Field(..., description="Comma separated tags")

class GenerateTagPayload(BaseModel):
    age_rating: str = Field(..., description="Age rating")
    description: str = Field(..., description="Game description")
    title: str = Field(..., description="Comma separated titles")


@app.post("/api/tags")
def read_root(payload: GenerateTagPayload):
    return generate_tags(dict(payload))


@app.post("/api/title")
def read_root(payload: GenerateTitlePayload):
    return generate_titles(dict(payload))