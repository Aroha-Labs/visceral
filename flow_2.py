import requests
import json
from dotenv import load_dotenv
import os

def flow_2(game_description):
    # Load environment variables from .env file
    load_dotenv()

    description = "for the below given game description generate 5 game titles \n description:{}".format(game_description)
    url = "https://serving.app.predibase.com/1054453e/deployments/v2/llms/llama-3-8b-instruct/generate"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {os.getenv('PREDIBASE_AUTH_TOKEN')}"
    }
    data = {
        "inputs": description,
        "parameters": {
            "adapter_id": "forntine-game-title/1",
            "adapter_source": "pbase",
            "max_new_tokens": 60,
            "temperature": 0.6
        }
    }

    try:
        response = requests.post(url, headers=headers, data=json.dumps(data))
        response.raise_for_status()  # Raises an HTTPError for bad responses (4xx and 5xx)
        # print(response.json())
        return response.json()['generated_text']
    except requests.exceptions.HTTPError as errh:
        return f"HTTP Error: {errh}"
    except requests.exceptions.ConnectionError as errc:
        return f"Error Connecting: {errc}"
    except requests.exceptions.Timeout as errt:
        return f"Timeout Error: {errt}"
    except requests.exceptions.RequestException as err:
        return f"Something went wrong: {err}"

# Example usage
# game_description = "Play in a band with friends or perform solo on stage with hit music by your favorite artists in Fortnite Festival! On the Main Stage, play a featured rotation of Jam Tracks. Compete against friends for the best performance or team up to climb the leaderboards. The festival is just beginning with more Jam Tracks, Music Icons, concerts, and stages coming soon. Take your stage in Fortnite Festival!"
# print(description)
# description = "for this game description generate 5 game titles {}".format(game_description)
# response = generate_response(description)
# print(response)

