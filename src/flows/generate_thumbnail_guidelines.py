import base64
import os
import mimetypes
import zipfile
from anthropic import Anthropic
from PIL import Image
import io

def get_image_mime_type(filename):
    mime_type, _ = mimetypes.guess_type(filename)
    return mime_type or "application/octet-stream"

def is_valid_image(image_data):
    try:
        Image.open(io.BytesIO(image_data))
        return True
    except:
        return False

def process_images(zip_file):
    anthropic = Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

    encoded_images = []
    for filename in zip_file.namelist():
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
            image_data = zip_file.read(filename)
            if not image_data or not is_valid_image(image_data):
                continue
            
            base64_image = base64.b64encode(image_data).decode('utf-8')
            mime_type = get_image_mime_type(filename)
            encoded_images.append((base64_image, mime_type))

    if not encoded_images:
        return {"error": "No valid images found in the zip file"}

    message_content = []
    for idx, (image_data, mime_type) in enumerate(encoded_images):
        message_content.extend([
            {
                "type": "text",
                "text": f"Image {idx + 1}:"
            },
            {
                "type": "image",
                "source": {
                    "type": "base64",
                    "media_type": mime_type,
                    "data": image_data,
                },
            }
        ])
    
    message_content.append({
        "type": "text",
        "text": """Analyze the composition of these thumbnail images. Identify trends in the position of characters, objects, and text. Consider:
1. Text placement
2. Character/object positioning
3. Background
4. Layout
5. Branding
6. Visual effects
7. Content showcase
Provide a detailed analysis of these factors only and nothing else."""
    })

    try:
        message = anthropic.messages.create(
            model="claude-3-5-sonnet-20240620",
            max_tokens=1024,
            messages=[
                {
                    "role": "user",
                    "content": message_content,
                }
            ],
        )
        
        return {"response": message.content[0].text}
    except Exception as e:
        return {"error": f"API Error: {str(e)}"}

