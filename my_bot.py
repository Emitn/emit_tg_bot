import os
import requests
from anyio import sleep
from dotenv import load_dotenv
import time

load_dotenv()

API_URL = os.getenv('API_URL')
BOT_TOKEN = os.getenv('BOT_TOKEN')

TEXT = "Nice update"

MAX_COUNTER = 100

offset: int = -2
counter: int = 0
chat_id: int

print(requests.get(f"{API_URL}{BOT_TOKEN}/getUpdates?offset=-1"))

while counter < MAX_COUNTER:
    print(f"attempt={counter}")
    updates = requests.get(f"{API_URL}{BOT_TOKEN}/getUpdates?offset={offset + 1}").json()

    if updates["result"]:
        for result in updates["result"]:
            offset = result["update_id"]
            chat_id = result["message"]["from"]["id"]
            requests.get(f"{API_URL}{BOT_TOKEN}/sendMessage?chat_id={chat_id}&text={TEXT}")
    time.sleep(1)
    counter += 1