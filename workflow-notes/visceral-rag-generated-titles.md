# Titles Generation using RAG

## Description
This script generates game titles using Large Language Models (LLMs) based on the game tags, description, and age rating. The model only uses data from games with the same age rating to generate relevant titles. Five potential titles will be generated for each game.

## Inputs
- **game_tags** (string): A list of generated tags for the game.
- **age_rating** (string): The age rating of the game.
- **description** (string): A brief description of the game.

## Outputs
- **game_titles** (list of strings): Five potential titles for the game.

## Examples

**Inputs:**
- **tags:** music
- **description:** Explore the Jam Stage festival grounds to find friends and stages where you can mix hit music using the Jam Tracks in your locker. The festival is just beginning with more Jam Tracks, Music Icons, concerts, and stages coming soon. Take your stage in Fortnite Festival!
- **age_rating:** Teen / 12

**Outputs:**
- **generated_titles:** 
<br>1. Jam Stage Jamboree 🎵🎸
<br>2. Harmonic Fest Frenzy 🎤🎶
<br>3. Melody Mania Main Stage 🎹🎵
<br>4. Rhythm Riot Festival Fun 🥁🔥
<br>5. Tune Town Showcase Spectacular 🎼🎸