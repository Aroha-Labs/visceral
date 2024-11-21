from enum import Enum
from pydantic import BaseModel, Field
from prometheus_fastapi_instrumentator import Instrumentator
from src.flows.title import generate_titles
from src.flows.tag import generate_tags
from src.flows.thumbnail_critique import generate_thumbnail_critique
from src.flows.generate_thumbnail_guidelines import process_images
from src.flows.data_management_services import upload_csv, fetch_csv, update_thumbnail_guidelines, fetch_recommended_thumbnails, title_tag_etl, fetch_thumbnail_guidelines
from fastapi import FastAPI, UploadFile, File, Form, HTTPException, Response
from fastapi.responses import FileResponse
from supabase import create_client, Client
import base64
import zipfile
import io
import os
from PIL import Image
import tempfile

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

@app.post("/api/data/upload-map-data")
async def upload_csv_endpoint(file: UploadFile = File(...)):
    csv_content = await file.read()
    csv_file = io.StringIO(csv_content.decode('utf-8'))
    result = upload_csv(csv_file, os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_KEY"), "training_data")
    return {"message": "CSV uploaded successfully"}

@app.get("/api/data/fetch-map-data")
async def fetch_csv_endpoint():
    csv_data = fetch_csv(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_KEY"), "training_data")
    
    # Create a temporary file to store the CSV data
    with tempfile.NamedTemporaryFile(mode='w+', delete=False, suffix='.csv') as temp_file:
        temp_file.write(csv_data)
        temp_file_path = temp_file.name

    # Use the temporary file path in FileResponse
    return FileResponse(
        temp_file_path,
        media_type="text/csv",
        filename="training_data.csv"
    )

@app.post("/api/data/update-thumbnail-guidelines")
async def update_thumbnail_guidelines_endpoint(genre: str = Form(...), guidelines: str = Form(...)):
    result = update_thumbnail_guidelines(genre, os.getenv("SUPABASE_KEY"), os.getenv("SUPABASE_URL"), "thumbnail_guidelines", guidelines)
    return {"message": "Thumbnail guidelines updated"}

@app.post("/api/data/upload-thumbnail-images-for-guidelines")
async def upload_thumbnail_images_for_guidelines(genre: str = Form(...), file: UploadFile = File(...)):
    supabase: Client = create_client(
        os.getenv("SUPABASE_URL"),
        os.getenv("SUPABASE_KEY")
    )
    
    try:
        # Read file and encode to Base64
        file_content = await file.read()
        base64_encoded_image = base64.b64encode(file_content).decode('utf-8')

        # Prepare data for Supabase table insertion
        table_name = "thumbnails_for_guidelines"
        data = {
            "genre": genre,
            "encoded_image": base64_encoded_image
        }
        
        # Insert the data into the Supabase table
        insert_response = supabase.table(table_name).insert(data).execute()
        
        return {"message": "Image uploaded successfully", "file_name": file.filename, "genre": genre}
    
    except Exception as e:
        return {"error": str(e)}


@app.post("/api/data/upload-recommended-thumbnails-by-genre")
async def upload_recommended_thumbnails_by_genre(genre: str = Form(...), file: UploadFile = File(...)):
    supabase: Client = create_client(
        os.getenv("SUPABASE_URL"),
        os.getenv("SUPABASE_KEY")
    )
    
    try:
        # Read file and encode to Base64
        file_content = await file.read()
        base64_encoded_image = base64.b64encode(file_content).decode('utf-8')

        # Prepare data for Supabase table insertion
        table_name = "recommended_thumbnails"
        data = {
            "genre": genre,
            "thumbnail": base64_encoded_image
        }
        
        # Check if genre already exists
        existing_entry = supabase.table(table_name).select("*").eq("genre", genre).execute()
        
        if existing_entry.data:
            # Update the existing entry
            update_response = supabase.table(table_name).update(data).eq("genre", genre).execute()
            message = "Image updated successfully"
        else:
            # Insert new entry
            insert_response = supabase.table(table_name).insert(data).execute()
            message = "Image uploaded successfully"
        
        return {"message": message, "file_name": file.filename, "genre": genre}
    
    except Exception as e:
        return {"error": str(e)}
    
@app.post("/api/data/title-tag-etl")
async def title_tag_etl_endpoint(file: UploadFile = File(...)):
    content = await file.read()
    processed_data = title_tag_etl(content)
    return  processed_data

@app.get("/api/data/fetch-recommended-thumbnails/{genre}")
async def fetch_recommended_thumbnails_endpoint(genre: str):
    image = fetch_recommended_thumbnails(genre, os.getenv("SUPABASE_KEY"), os.getenv("SUPABASE_URL"), "recommended_thumbnails")
    if image:
        # Convert PIL Image to bytes
        img_byte_arr = io.BytesIO()
        image.save(img_byte_arr, format='PNG')
        img_byte_arr = img_byte_arr.getvalue()
        return Response(content=img_byte_arr, media_type="image/png")
    else:
        raise HTTPException(status_code=404, detail="Image not found")

@app.get("/api/data/fetch-thumbnail-guidelines/{genre}")
async def fetch_thumbnail_guidelines_endpoint(genre: str):
    guidelines = fetch_thumbnail_guidelines(
        genre, 
        os.getenv("SUPABASE_KEY"), 
        os.getenv("SUPABASE_URL"), 
        "thumbnail_guidelines"
    )
    if guidelines:
        return guidelines
    else:
        raise HTTPException(status_code=404, detail="Guidelines not found")


@app.post("/api/generate/generate-title")
async def generate_title_endpoint(payload: GenerateTitlePayload):
    return generate_titles(dict(payload))

@app.post("/api/generate/generate-tags")
async def generate_tags_endpoint(payload: GenerateTagPayload):
    return generate_tags(dict(payload))

@app.post("/api/generate/generate-thumbnail-critique")
async def generate_thumbnail_critique_endpoint(
    genre: str = Form(...),
    image: UploadFile = File(...)
):
    payload = {"genre": genre}
    return generate_thumbnail_critique(payload, image)

@app.post("/api/generate/generate-thumbnail-guidelines")
async def generate_thumbnail_guidelines_endpoint(file: UploadFile = File(...)):
    zip_contents = await file.read()
    zip_file = zipfile.ZipFile(io.BytesIO(zip_contents))
    return process_images(zip_file)

@app.get("/health")
def health_check():
    return {"status": "OK"}
