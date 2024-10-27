# Visceral System Documentation

## System Overview
A comprehensive Visceral system for managing Fortnite map content through data management and generation services, leveraging LLMs for content generation.

## API Reference

### Data Management Service
- `upload_csv`
  - Purpose: Upload CSV file containing title and tag data for processing
  - Input: CSV file
  - Note: At any time we have only once csv

- `fetch_csv`
  - Purpose: Retrieve previously uploaded title and tag data
  - Output: CSV data

- `updated_thumbnail_guidelines`
  - Purpose: Update the thumbnail guidelines
  - Input: text - genre, guidelines
  - Note: This is a manual process 

- `upload_thumbnail_images_for_guidelines`
  - Purpose: Upload reference images for guideline creation
  - Input: Image files

- `upload_recommended_thumbnails_by_genre`
  - Purpose: Upload genre-specific recommended thumbnails
  - Input: Categorized image files
  - Note: This is manually generated

- `title_etl`
  - Purpose: Process and transform title data
  - Input: Raw title data
  - Output: Processed title data

- `tag_etl`
  - Purpose: Process and transform tag data
  - Input: Raw tag data
  - Output: Processed tag data

- `fetch_recommended_thumbnails`
  - Purpose: Retrieve recommended thumbnail guidelines
  - Output: Stored thumbnail guidelines

### Generation Service (LLM-based)
- `generate_title`
  - Purpose: Create optimized titles using processed data
  - Input: Processed data
  - Output: Generated title
  - Note: Uses LLM for generation

- `generate_tags`
  - Purpose: Create relevant tags using processed data
  - Input: Processed data
  - Output: Generated tags
  - Note: Uses LLM for generation

- `generate_critique_thumbnail`
  - Purpose: Create critique by analyzing the thumbnails
  - Input: Thumbnail image
  - Output: Analysis feedback
  - Note: Uses LLM for analysis

- `generate_thumbnail_guidelines`
  - Purpose: Create guidelines for thumbnail generation
  - Output: Thumbnail creation guidelines
  - Note: Uses LLM for guideline generation
  - Internal Process, we uploaded the thumbnails in claude, get the guidelines and update them

## V2
- title & tag data management has to move to postgres completely
- automate the guidelines
