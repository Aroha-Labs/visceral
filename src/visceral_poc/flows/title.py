import pandas as pd
from openai import OpenAI

client = OpenAI()

train_df = pd.read_csv("./train.csv")


def rag_flow(prompt):
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": "You are a assistant, skilled in suggesting game titles with a creative flair.",
            },
            {"role": "user", "content": prompt},
        ],
    )

    return completion.choices[0].message.content


# input = { description, age_rating, tags }
def generate_titles(input: dict):
    """
    Generate 5 game titles based on the input description, age rating and tags.
    """
    base_prompt = """{}
Based on the above game data, for this game description, age rating and tags generate 5 game titles. Return the titles only and no other text.
{}
"""
    age_rating = input["age_rating"]
    tags = input["tags"]
    description = input["description"]

    filtered_df = train_df[train_df["Age Rating"] == age_rating]
    retrieved_text = filtered_df.to_string()
    input_text = description + "\n" + age_rating + "\n" + tags
    prompt = base_prompt.format(retrieved_text, input_text)
    generated_title = rag_flow(prompt)

    return generated_title


# print(
#     generate_titles(
#         {
#             "Description": "A game about a detective solving a",
#             "Age Rating": "12+",
#             "Tags": "Adventure, Puzzle",
#         }
#     )
# )
