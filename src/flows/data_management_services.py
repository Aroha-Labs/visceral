import csv
import io
import pandas as pd
from supabase import create_client, Client
import os
import base64
from PIL import Image

def upload_csv(csv_file_path: str, supabase_url: str, supabase_key: str, table_name: str):
    # Initialize Supabase client
    supabase: Client = create_client(supabase_url, supabase_key)

    # Read CSV file
    df = pd.read_csv(csv_file_path, index_col=0)  # Ignore the index column

    # Convert DataFrame to list of dictionaries
    records = df.to_dict('records')

    try:
        # Clear existing data in the table
        supabase.table(table_name).delete().neq('id', 0).execute()

        # Insert new data
        response = supabase.table(table_name).insert(records).execute()

        print(f"Successfully uploaded {len(records)} records to {table_name}")
        return response
    except Exception as e:
        print(f"Error uploading data to Supabase: {str(e)}")
        return None

def fetch_csv(supabase_url: str, supabase_key: str, table_name: str):
    # Initialize Supabase client
    supabase: Client = create_client(supabase_url, supabase_key)

    try:
        # Fetch all data from the table
        response = supabase.table(table_name).select('*').execute()
        
        # Extract the data from the response
        data = response.data

        # Convert to DataFrame
        df = pd.DataFrame(data)

        # Remove 'id' column if it exists
        if 'id' in df.columns:
            df = df.drop('id', axis=1)

        # Reset index to add a new index column
        df = df.reset_index(drop=True)

        # Convert DataFrame to CSV string
        csv_string = df.to_csv(index=True)

        return csv_string

    except Exception as e:
        print(f"Error fetching data from Supabase: {str(e)}")
        return None

def update_thumbnail_guidelines(genre: str, supabase_key: str, supabase_url: str, table_name: str, guidelines: str):
    # Create Supabase client
    supabase = create_client(supabase_url, supabase_key)

    # Check if genre exists
    result = supabase.table(table_name).select("*").eq("genre", genre).execute()
    
    if len(result.data) > 0:
        # Genre exists, update guidelines
        response = supabase.table(table_name).update({"guidelines": guidelines}).eq("genre", genre).execute()
    else:
        # Genre doesn't exist, insert new entry
        response = supabase.table(table_name).insert({"genre": genre, "guidelines": guidelines}).execute()
    
    return response.data

def fetch_recommended_thumbnails(genre: str, supabase_key: str, supabase_url: str, table_name: str):
    supabase = create_client(supabase_url, supabase_key)
    try:
        # Fetch the thumbnail for the specified genre
        response = supabase.table(table_name).select("thumbnail").eq("genre", genre).execute()
        
        if response.data and len(response.data) > 0:
            # Extract the base64 encoded image
            base64_image = response.data[0]['thumbnail']
            
            # Decode the base64 string
            image_data = base64.b64decode(base64_image)
            
            # Create a BytesIO object from the decoded data
            image_buffer = io.BytesIO(image_data)
            
            # Open the image using PIL
            image = Image.open(image_buffer)
            
            return image
        else:
            print(f"No thumbnail found for genre: {genre}")
            return None
    except Exception as e:
        print(f"Error fetching thumbnail from Supabase: {str(e)}")
        return None

def title_tag_etl(data: str) -> str:
    try:
        # Determine if the data is CSV or Excel
        if data.startswith("PK"):  # Excel files start with "PK"
            # Read Excel data into a DataFrame
            df = pd.read_excel(io.BytesIO(data.encode()))
        else:
            # Read CSV data into a DataFrame
            df = pd.read_csv(io.StringIO(data))
        
        # Select specific columns
        select = df[['Genre', 'Map Name', 'Description', 'Age Rating', 'Tags']]
        
        # Filter out rows where Description is 'NOT FOUND'
        select = select[select['Description'] != 'NOT FOUND']
        
        # Convert the processed DataFrame back to CSV string
        processed_csv = select.to_csv(index=False)
        
        return processed_csv
    except Exception as e:
        print(f"Error processing CSV data: {str(e)}")
        return None

