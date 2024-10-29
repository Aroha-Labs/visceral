# API Documentation

## Data Management Endpoints

### Upload Training Data
- **POST** `/api/data/upload-map-data`
- Uploads CSV training data to Supabase
- **Input**: CSV file


### Fetch Training Data
- **GET** `/api/data/fetch-map-data`
- Downloads the current training dataset
- **Response**: CSV file

### Update Thumbnail Guidelines
- **POST** `/api/data/update-thumbnail-guidelines`
- Updates or creates thumbnail guidelines for a specific genre
- **Input**: 
  - `genre`: Game genre
  - `guidelines`: Thumbnail design guidelines


### Upload Thumbnail Images for Guidelines
- **POST** `/api/data/upload-thumbnail-images-for-guidelines`
- Uploads reference images for thumbnail guidelines
- **Input**:
  - `genre`: Game genre
  - `file`: Image file


### Upload Recommended Thumbnails
- **POST** `/api/data/upload-recommended-thumbnails-by-genre`
- Uploads or updates recommended thumbnails for a genre
- **Input**:
  - `genre`: Game genre
  - `file`: Thumbnail image


### Fetch Recommended Thumbnails
- **GET** `/api/data/fetch-recommended-thumbnails/{genre}`
- Retrieves recommended thumbnail for specified genre
- **Response**: PNG image

### Process Title and Tag Data
- **POST** `/api/data/title-tag-etl`
- Processes and transforms title and tag data
- **Input**: CSV/Excel file
- **Response**: Processed CSV data

### Fetch Thumbnail Guidelines
- **GET** `/api/data/fetch-thumbnail-guidelines/{genre}`
- Retrieves thumbnail design guidelines for specified genre
- **Response**: 
  ```json
  {
    "guidelines": "string"
  }
  ```

## Generation Endpoints

### Generate Title
- **POST** `/api/generate/generate-title`
- Generates game titles based on input parameters
- **Input**:
  ```json
  {
    "age_rating": "string",
    "description": "string",
    "genre": "string",
    "max_title_length": "integer",
    "max_word_length": "integer",
    "title_style": "string"
  }
  ```
- **Response**: Comma-separated list of generated titles

### Generate Tags
- **POST** `/api/generate/generate-tags`
- Generates relevant tags for a game
- **Input**:
  ```json
  {
    "age_rating": "string",
    "description": "string",
    "title": "string",
    "genre": "string",
    "exclude_tags": "string"
  }
  ```
- **Response**: Comma-separated list of generated tags

### Generate Thumbnail Critique
- **POST** `/api/generate/generate-thumbnail-critique`
- Analyzes and critiques game thumbnails
- **Input**:
  - `genre`: Game genre
  - `image`: Thumbnail image file
- **Response**: Detailed critique and suggestions

### Generate Thumbnail Guidelines
- **POST** `/api/generate/generate-thumbnail-guidelines`
- Analyzes multiple thumbnails to generate guidelines
- **Input**: ZIP file containing thumbnail images
- **Response**: Analysis of thumbnail composition trends

