import pandas as pd
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI()

train_df = pd.read_csv('train.csv')
test_df = pd.read_csv('test.csv')

def rag_flow(prompt):
    completion = client.chat.completions.create(
      model="gpt-3.5-turbo",
      messages=[
        {"role": "system", "content": "You are a assistant, skilled in suggesting game titles with a creative flair."},
        {"role": "user", "content": prompt}
      ]
    )

    return completion.choices[0].message.content

base_prompt = """{}
Based on the above game data, for this game description, age rating and tags generate 5 game titles. Return the titles only and no other text.
{}
"""

for index, row in test_df.iterrows():
    age_rating = row.iloc[2]
    filtered_df = train_df[train_df['Age Rating'] == age_rating]
    retrieved_text = filtered_df.to_string()
    input_text = row.iloc[[1, 2, 3]].to_string()
    prompt = base_prompt.format(retrieved_text,input_text)
    print("Actual Title : ",row.iloc[0])
    print("Generated Titles :\n",rag_flow(prompt))


