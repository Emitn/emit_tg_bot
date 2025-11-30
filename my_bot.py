import os
import requests
from dotenv import load_dotenv
import time

load_dotenv()

API_URL = os.getenv('API_URL')
BOT_TOKEN = os.getenv('BOT_TOKEN')
API_CATS_URL = "https://api.thecatapi.com/v1/images/search"
ERROR_TEXT = "NO_CAT"

TEXT = "Nice update"

MAX_COUNTER = 100

offset: int = -2
counter: int = 0
chat_id: int
cat_response: requests.Response
cat_link: str


while counter < MAX_COUNTER:
    print(f"attempt={counter}")
    updates = requests.get(f"{API_URL}{BOT_TOKEN}/getUpdates?offset={offset + 1}&timeout=60").json()

    if updates["result"]:
        for result in updates["result"]:
            offset = result["update_id"]
            chat_id = result["message"]["from"]["id"]
            cat_response = requests.get(API_CATS_URL)
            if cat_response.status_code == 200:
                cat_link = cat_response.json()[0]["url"]
                echo_message = f"{result["message"]["text"]} is nice, but cat photo is better"
                requests.get(f"{API_URL}{BOT_TOKEN}/sendMessage?chat_id={chat_id}&text={echo_message}")
                requests.get(f"{API_URL}{BOT_TOKEN}/sendPhoto?chat_id={chat_id}&photo={cat_link}")
            else:
                requests.get(f"{API_URL}{BOT_TOKEN}/sendMessage?chat_id={chat_id}&text={ERROR_TEXT}")
    time.sleep(1)
    counter += 1