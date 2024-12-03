A API service for game asset generation and management, including title generation, tag generation, and thumbnail analysis.

## Features

- Title Generation: Generate game titles based on various parameters
- Tag Generation: Create relevant tags for games
- Thumbnail Analysis: Analyze and critique game thumbnails
- Data Management: Upload and manage game-related data
- Guidelines Generation: Create thumbnail design guidelines

## Project Structure

```
visceral-poc/
├── src/                    # Source code directory
│   ├── flows/             # Flow implementations
│   └── visceral_poc/      # Core application code
├── sql_schema/            # Database initialization scripts
│   ├── 01_thumbnail_guidelines.sql
│   ├── 02_recommended_thumbnails.sql
│   ├── 03_training_data.sql
│   └── 04_thumbnails_for_guidelines.sql
├── docker-compose.yml     # Docker Compose configuration
├── Dockerfile            # Docker configuration
├── pyproject.toml        # Python project configuration
├── pdm.lock             # PDM lock file
```

## Prerequisites

- Docker
- Docker Compose 
- Python 3.10 or higher (for local development)
- PDM (Python Dependency Manager)


## Database Setup

1. Log in to your Supabase project dashboard.

2. Navigate to the SQL Editor in your Supabase dashboard.

3. Execute the SQL schema files in the following order:
   - `sql_schema/01_thumbnail_guidelines.sql`: Sets up thumbnail guidelines tables
   - `sql_schema/02_recommended_thumbnails.sql`: Creates recommended thumbnails structure
   - `sql_schema/03_training_data.sql`: Initializes training data tables
   - `sql_schema/04_thumbnails_for_guidelines.sql`: Sets up thumbnails for guidelines tables

These schemas will set up all necessary tables and relationships required for the application to function properly.

## Quick Start with Docker

1. Clone the repository:
   ```bash
   git clone https://github.com/Aroha-Labs/visceral-poc
   cd visceral-poc
   ```

2. Create your environment file:
   ```bash
   cp .env.example .env
   ```
   Edit `.env` with your configuration values.

3. Build and run with Docker using one of the following profiles:

   - For local development:
     ```bash
     docker compose --profile local up --build
     ```
     The API will be available at `http://localhost:8000`

   - For staging environment:
     ```bash
     docker compose --profile stg up --build
     ```

   - For production environment:
     ```bash
     docker compose --profile prod up --build
     ```

   Note: Staging and production environments include GELF logging configuration for log aggregation.

## Local Development Setup

1. Install PDM (Python Dependency Manager):  
   ```bash
   pip install pdm
   ```

2. Initialize the project:
   ```bash
   # Navigate to project directory
   cd visceral-poc
   
   # Initialize PDM environment (this creates a virtual environment)
   pdm install
   ```

3. Run the development server:
   ```bash
   # This command is defined in pyproject.toml and starts the API server
   pdm start
   ```

   Note: PDM is a modern Python package manager that handles dependencies more efficiently than pip. It's similar to npm for Node.js or cargo for Rust.

## API Documentation

For detailed API documentation, please see [api_documentation.md](api_documentation.md)
