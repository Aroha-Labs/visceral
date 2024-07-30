import pandas as pd
from openai import OpenAI
import json

client = OpenAI()

train_df = pd.read_csv("./train.csv")


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
    Generate 5 game titles based on the input description, age rating and tags.
    """
    base_prompt = """{}
Based on the above game data, for this game description, age rating and tags generate 5 game titles with each title not exceeding 15 characters. Return the titles only and no other text in the format ["title1","title2","title3","title4","title5"].
{}
"""
    age_rating = input["age_rating"]
    tags = input["tags"]
    description = input["description"]
    max_title_length = input["max_title_length"]
    max_word_length = input["max_word_length"]

    filtered_df = train_df[train_df["Age Rating"] == age_rating]
    retrieved_text = filtered_df.to_string()
    input_text = description + "\n" + age_rating + "\n" + tags
    prompt = base_prompt.format(retrieved_text, input_text)
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
#             "description": "A game about a detective solving a",
#             "age_rating": "12+",
#             "tags": "Adventure, Puzzle",
#             "max_title_length": 15,
#             "max_word_length": 6,
#         }
#     )
# )
