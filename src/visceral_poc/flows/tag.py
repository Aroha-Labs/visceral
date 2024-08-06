import pandas as pd
from openai import OpenAI
import json


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

game_tags = [s.lower() for s in game_tags]

train_df = pd.read_csv("./training(6-8-24).csv")
# test_df = pd.read_csv("evalset.csv")


def rag_flow(prompt):
    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "system",
                "content": "You are a assistant, skilled in suggesting game tags.",
            },
            {"role": "user", "content": prompt},
        ],
    )

    return completion.choices[0].message.content

def get_tags(prompt):
    generated_tags = rag_flow(prompt)
    items_list = json.loads(generated_tags)
    return items_list

# input = { description, age_rating, title }
def generate_tags(input: dict):
    base_prompt = """{}
Based on the above game data, for this game title,game description, age rating and genre suggest 4 game tags out of {}. The tags should belong to the list only and adhere to the list. Return the game tag only and no other text.
Response should strictly follow the below format:
["tag1", "tag2", "tag3", "tag4"]
{}
"""
    age_rating = input["age_rating"]
    title = input["title"]
    description = input["description"]
    genre = input["genre"]

    filtered_df = train_df[train_df["Genre"] == genre]
    retrieved_text = filtered_df.to_string()
    input_text = description + "\n" + age_rating + "\n" + title + "\n" + genre
    prompt = base_prompt.format(retrieved_text, game_tags, input_text)
    tags=[]
    for iter in range(5):
        for tag in get_tags(prompt):
            if tag not in tags and tag in game_tags:
                tags.append(tag)
            if len(tags) == 4:
                break
        if len(tags) == 4:
                break

    return tags


# print(
#     generate_tags(
#         {
#             "description": "📦 CLASSIC BOX FIGHTS🐠 BOXED LIKE A FISH🤯 200 PUMP IS BACK🏆 WINNER GETS GOLD PUMP💾 ELIMINATIONS & WINS SAVE",
#             "age_rating": "12+",
#             "title": "BOX PVP 📦",
#             "genre": "PvP"
#         }
#     )
# )
