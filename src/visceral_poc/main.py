from enum import Enum
from pydantic import BaseModel, Field
from prometheus_fastapi_instrumentator import Instrumentator
from src.flows.title import generate_titles
from src.flows.tag import generate_tags
from src.flows.thumbnail_critique import generate_thumbnail_critique
from fastapi import FastAPI, UploadFile, File, Form
from supabase import create_client, Client
import base64
import os

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
    title_style: str = Field(..., description="Title Style")


class GenerateTagPayload(BaseModel):
    age_rating: str = Field(..., description="Age rating")
    description: str = Field(..., description="Game description")
    title: str = Field(..., description="Comma separated titles")
    genre: str = Field(..., description="Game genre")
    exclude_tags: str = Field(..., description="Comma separated tags to exclude")

class GenerateThumbnailCritiquePayload(BaseModel):
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


@app.post("/api/thumbnail-critique")
async def thumbnail_critique(
    genre: str = Form(...),
    image: UploadFile = File(...)
):
    payload = {"genre": genre}
    return generate_thumbnail_critique(payload, image)

@app.post("/upload-image/")
async def upload_image(file: UploadFile = File(...)):
    supabase: Client = create_client(
        os.getenv("SUPABASE_URL"),
        os.getenv("SUPABASE_KEY")
    )
    
    try:
        # Read file and encode to Base64
        file_content = await file.read()
        base64_encoded_image = base64.b64encode(file_content).decode('utf-8')

        # Prepare data for Supabase table insertion
        table_name = "visceral-files"
        data = {
            "file_name": file.filename,
            "encoded_image": base64_encoded_image
        }
        
        # Insert the data into the Supabase table
        insert_response = supabase.table(table_name).insert(data).execute()
        
        return {"message": "Image uploaded successfully", "file_name": file.filename}
    
    except Exception as e:
        return {"error": str(e)}
