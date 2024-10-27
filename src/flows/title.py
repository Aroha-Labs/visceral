import pandas as pd
from openai import OpenAI
import json
from src.flows.data_management_services import fetch_csv
import os
import io


supabase_url = os.getenv("SUPABASE_URL")
supabase_key = os.getenv("SUPABASE_KEY")
table_name = "training_data"
csv_string = fetch_csv(supabase_url, supabase_key, table_name)
train_df = pd.read_csv(io.StringIO(csv_string))
client = OpenAI()

def rag_flow(prompt):
    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "system",
                "content": "You are a assistant, skilled in suggesting game titles with a creative flair.",
            },
            {"role": "user", "content": prompt},
        ],
    )

    return completion.choices[0].message.content

def get_titles(prompt):
    generated_title = rag_flow(prompt)
    items_list = json.loads(generated_title)
    return items_list

# input = { description, age_rating, tags }
def generate_titles(input: dict):
    """
    Generate 5 game titles based on the input description, age rating and genre.
    """
    base_prompt = """{}
Based on the above game data, for this game description, age rating and genre generate 5 game titles in the {} style. Return the titles only and no other text in the format ["title1","title2","title3","title4","title5"].
{}
"""
    age_rating = input["age_rating"]
    genre = input["genre"]
    description = input["description"]
    max_title_length = input["max_title_length"]
    max_word_length = input["max_word_length"]
    title_style = input["title_style"]

    if(title_style == "optimal"):
        title_style = "above"

    filtered_df = train_df[train_df["Genre"] == genre]
    retrieved_text = filtered_df.to_string()
    input_text = description + "\n" + age_rating + "\n" + genre
    prompt = base_prompt.format(retrieved_text, title_style, input_text)
    titles = []
    while len(titles) < 5:
        for title in get_titles(prompt):
            if title not in titles and len(title) < max_title_length and all(len(word) < max_word_length for word in title.split()):
                titles.append(title)
            if len(titles) == 5:
                break
    return ', '.join(titles)


# print(
#     generate_titles(
#         {
#             "description": "📦 CLASSIC BOX FIGHTS🐠 BOXED LIKE A FISH🤯 200 PUMP IS BACK🏆 WINNER GETS GOLD PUMP💾 ELIMINATIONS & WINS SAVE",
#             "age_rating": "12+",
#             "genre":"PvP",
#             "max_title_length": 25,
#             "max_word_length": 7,
#             "title_style": "optimal"
#         }
#     )
# )
