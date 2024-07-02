# Tags Generation using RAG

## Description
This script generates game tags using Large Language Models (LLMs) based on the game title, description, and age rating. The model only uses data from games with the same age rating to generate relevant tags. A maximum of four tags can be generated for each game.

## Inputs
- **game_title** (string): The title of the game.
- **age_rating** (string): The age rating of the game.
- **description** (string): A brief description of the game.

## Outputs
- **game_tags** (list of strings): A list of generated tags for the game.

## Examples

**Inputs:**
- **title:** Festival Jam Stage
- **description:** Explore the Jam Stage festival grounds to find friends and stages where you can mix hit music using the Jam Tracks in your locker. The festival is just beginning with more Jam Tracks, Music Icons, concerts, and stages coming soon. Take your stage in Fortnite Festival!
- **age_rating:** Teen / 12

**Outputs:**
- **generated_tags:** ["music", "party game", "casual", "competition"]