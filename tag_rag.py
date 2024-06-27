import pandas as pd
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI()


game_tags = [
    "2D",
    "1v1",
    "2v2",
    "3v3",
    "4v4",
    "5v5",
    "6v6",
    "7v7",
    "8v8",
    "Action",
    "Adventure",
    "Aim Course",
    "Arcade",
    "Arena",
    "Artistic",
    "Atmospheric",
    "Attack",
    "Base",
    "Base Building",
    "Battle",
    "Battle Royale",
    "Board Game",
    "Boss Battle",
    "Boxfight",
    "Building",
    "Capture the Flag",
    "Card Game",
    "Casual",
    "Choices Matter",
    "Classes",
    "Clicker",
    "Co-op",
    "Collection",
    "Competitive",
    "Crafting",
    "Creatures",
    "Defend",
    "Difficulty: Easy",
    "Difficulty: Medium",
    "Difficulty: Hard",
    "Difficulty: Very Hard",
    "Difficulty: Ultra Hard",
    "Difficulty: Impossible",
    "Duo",
    "Driver Simulator",
    "Economy",
    "Edit Course",
    "Educational",
    "Episodic",
    "Escape",
    "Event",
    "Exploration",
    "Explosives",
    "Farming Simulator",
    "Fashion",
    "Fighting",
    "Fortnitemares",
    "Free for All",
    "Friendly",
    "Funny",
    "Gun Fight",
    "Gun Game",
    "Hardcore",
    "Heroes",
    "Horror",
    "Hub",
    "Infection",
    "Jam System",
    "Just for Fun",
    "King of the Hill",
    "Memes",
    "Melee",
    "Minigame",
    "Mining",
    "MOBA",
    "Moving",
    "Music",
    "Mystery",
    "Nonlinear",
    "Objective",
    "One in the Chamber",
    "One Life",
    "One Shot",
    "Open World",
    "Parkour",
    "Party Game",
    "Party World",
    "Patchwork",
    "Peaceful",
    "Pinball",
    "Point Capture",
    "Physics",
    "Pixel Art",
    "Platformer",
    "Practice",
    "Prop",
    "Prop Hunt",
    "Puzzle",
    "PVE",
    "PVP",
    "Quiz",
    "Race",
    "Respawn",
    "Retro",
    "Roguelike",
    "Role Playing",
    "RPG",
    "Rounds",
    "Runner",
    "Sandbox",
    "Search & Destroy",
    "Seasonal",
    "Secrets",
    "Sequel",
    "Series",
    "Shooter",
    "Shop",
    "Show",
    "Side Scroller",
    "Simulator",
    "Single Player",
    "Skillrun",
    "Skills",
    "Sniper",
    "Solo",
    "Space",
    "Sports",
    "Squad",
    "Stealth",
    "Story",
    "Strategy",
    "Survival",
    "Survival Horror",
    "Team Free for All",
    "Teams",
    "Timed",
    "Top-Down",
    "Tower Defense",
    "Training",
    "Trios",
    "Trivia",
    "Turn-Based",
    "Tutorial",
    "Tycoon",
    "Unbalanced Teams",
    "Visual Novel",
    "Winterfest",
    "Word Games",
    "ZoneWars",
]

train_df = pd.read_csv("train.csv")
test_df = pd.read_csv("evalset.csv")


def rag_flow(prompt):
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": "You are a assistant, skilled in suggesting game tags.",
            },
            {"role": "user", "content": prompt},
        ],
    )

    return completion.choices[0].message.content


base_prompt = """{}
Based on the above game data, for this game title,game description, age rating suggest a single game tag out of {}. Return the game tag only and no other text.
{}
"""
suggested_tags = []
for index, row in test_df.iterrows():
    age_rating = row["Age Rating"]
    filtered_df = train_df[train_df["Age Rating"] == age_rating]
    retrieved_text = filtered_df.to_string()
    input_text = row[["Game ", "Description", "Age Rating"]].to_string(
        index=False, header=False
    )
    prompt = base_prompt.format(retrieved_text, game_tags, input_text)
    suggested_tag = rag_flow(prompt)
    suggested_tags.append(suggested_tag)

    print("Actual Tag:", row["Tags"])
    print("Generated Titles:\n", suggested_tag)

test_df["Generated Tag"] = suggested_tags
output_csv = "rag_generated_tags.csv"
test_df.to_csv(output_csv, index=False)
