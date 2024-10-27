import base64
import requests
import os
from supabase import create_client, Client

# OpenAI API Key
api_key = os.environ.get("OPENAI_API_KEY")

# Supabase configuration
supabase_url = os.environ.get("SUPABASE_URL")
supabase_key = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(supabase_url, supabase_key)

# Function to encode the image
def encode_image(image_file):
  return base64.b64encode(image_file.read()).decode('utf-8')

def fetch_genre_guidelines(genre):
    response = supabase.table("thumbnail_guidelines").select("guidelines").eq("genre", genre).execute()
    if response.data:
        return response.data[0]['guidelines']
    else:
        return f"No guidelines found for genre: {genre}"

def generate_thumbnail_critique(payload, image):
    genre = payload['genre']

    genre_guidelines = fetch_genre_guidelines(genre)
    base64_image = encode_image(image.file)

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    payload = {
        "model": "gpt-4o",
        "messages": [
            {
                "role": "system",
                "content": f"You are an expert in game thumbnail design. Use these genre-specific guidelines: {genre_guidelines}"
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": f"Analyze this game thumbnail for the {genre} genre. Provide a critique and suggestions for improvement based on the genre guidelines."
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}"
                        }
                    }
                ]
            }
        ],
        "max_tokens": 500
    }

    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
    
    return response.json()["choices"][0]["message"]["content"]
