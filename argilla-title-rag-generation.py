import argilla as rg
import pandas as pd
from argilla._constants import DEFAULT_API_KEY

df = pd.read_csv("finetune_generated_titles.csv")

game_titles, game_descriptions, age_ratings, tags, generated_game_titles = (
    df["Game "].to_list(),
    df["Description"].to_list(),
    df["Age Rating"].to_list(),
    df["Tags"].to_list(),
    df['Generated Title'].to_list()
)

api_url = "https://argilla.lmnorg.xyz/"

client = rg.init(
    api_url=api_url,
    api_key=DEFAULT_API_KEY,
    workspace="argilla",
)

def create_dataset(dataset_name: str, workspace_name: str):
    dataset = rg.FeedbackDataset(
        guidelines="Review each of the field and provide feedback wherever necessary",
        fields=[
            rg.TextField(
                name="game_title",
                title="Original Game Title",
                use_markdown=True,
            ),
            rg.TextField(
                name="game_description",
                title="Input : Game Description",
                use_markdown=True,
            ),
            rg.TextField(
                name="age_rating",
                title="Input : Age Rating",
                use_markdown=True,
            ),
            rg.TextField(
                name="game_tags",
                title="Input : Game Tags",
                use_markdown=True,
            ),

            rg.TextField(
                name="generated_game_titles",
                title="Machine Generated Titles",
                use_markdown=True,
            ),
        ],

        questions=[
            rg.RatingQuestion(
                name="rating",
                title="Rate the quality of the generated response",
                description="1 : very bad ; 5 : excellent",
                values=[1, 2, 3, 4, 5],
                required=True,
            ),
            rg.TextQuestion(
                name="revised_generated_game_titles",
                title="Suggest a list of better game titles",
                required=False,
                use_markdown=True,
            ),
            rg.TextQuestion(
                name="user_suggestions",
                title="Expert Feedback",
                required=False,
                use_markdown=True,
            ),
        ],
    )

    dataset.push_to_argilla(name=dataset_name, workspace=workspace_name)

    print("Process successfully executed!")

    return dataset

def create_and_push_record(
    game_titles, game_descriptions, age_ratings, tags, generated_game_titles, dataset_name, workspace_name
):

    feedbackDB = rg.FeedbackDataset.from_argilla(
        name=dataset_name, workspace=workspace_name
    )

    for i in range(len(game_titles)):
        record = rg.FeedbackRecord(
            fields={
                "game_title": game_titles[i],
                "game_description": game_descriptions[i],
                "age_rating": age_ratings[i],
                "game_tags": tags[i],
                "generated_game_titles": generated_game_titles[i],
            },
            suggestions=[
                rg.SuggestionSchema(
                    question_name="revised_generated_game_titles", value=generated_game_titles[i]
                ),
                rg.SuggestionSchema(
                    question_name="user_suggestions",
                    value="Provide feedback for the generated response",
                ),
            ],
        )

        feedbackDB.add_records(record)

    print("Dataset pushed successfully!")


dataset = create_dataset("visceral_finetuned_generated_titles", "argilla")

create_and_push_record(
    game_titles, game_descriptions, age_ratings, tags, generated_game_titles, "visceral_finetuned_generated_titles", "argilla"
)