import os
from dotenv import load_dotenv
import requests

from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.types import Message, ContentType

from random import randint

load_dotenv()
BOT_TOKEN = os.getenv('BOT_TOKEN')

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

ATTEMPTS = 5

users = {}


def add_new_user(users_dict, user_id: int):
    if user_id not in users_dict:
        users_dict[user_id] = {"in_game" : False,
                               "secret_number" : None,
                               "attempts" : None,
                               "games" : 0,
                               "wins": 0}

@dp.message(Command(commands="waifu"))
async def process_waifu_command(message: Message):
    waifu_response = requests.get("https://api.waifu.im/search")
    await message.answer_photo(waifu_response.json()['images'][0]["url"])

@dp.message(Command(commands="start"))
async def process_start_command(message: Message):
    add_new_user(users, message.from_user.id)
    await message.answer("Hi. Lets play guess the number\n\n/help for rules")

@dp.message(Command(commands="help"))
async def process_help_command(message: Message):
    await message.answer(f"Rules: I choose number between 1 and 100, and you guess it\n"
                         f"You have {ATTEMPTS} attempts\n"
                         f"Available commands:\n"
                         f"/help - rules\n"
                         f"/stat - your statistics\n"
                         f"/cancel - leave the game\n")

@dp.message(Command(commands="stat"))
async  def process_stat_command(message: Message):
    add_new_user(users, message.from_user.id)
    await message.answer(f"Games played: {users[message.from_user.id]["games"]}\n"
                         f"Games won: {users[message.from_user.id]["wins"]}")

@dp.message(F.text.lower().in_(["yes", "y", "ok"]))
async def process_positive_answer(message: Message):
    add_new_user(users, message.from_user.id)
    if not users[message.from_user.id]["in_game"]:
        users[message.from_user.id]["in_game"] = True
        users[message.from_user.id]["secret_number"] = randint(1, 100)
        users[message.from_user.id]["attempts"] = ATTEMPTS
        await message.answer(f"I choose the number. Try to guess")
    else:
        await message.answer("We are already playing")

@dp.message(F.text.lower().in_(["no","n", "nah"]))
async  def process_negative_answer(message: Message):
    add_new_user(users, message.from_user.id)
    if not users[message.from_user.id]["in_game"]:
        await message.answer("Ok. Write me if you change your mind")
    else:
        await message.answer("We are already playing")

@dp.message(lambda x : x.text and x.text.isdigit() and 1 <= int(x.text) <= 100)
async def process_number(message: Message):
    add_new_user(users, message.from_user.id)
    if not users[message.from_user.id]["in_game"]:
        await message.answer("We don't play. Want to?")
    elif int(message.text) == users[message.from_user.id]["secret_number"]:
        users[message.from_user.id]["in_game"] = False
        users[message.from_user.id]["games"] += 1
        users[message.from_user.id]["wins"] += 1
        await message.answer("Right. You won. Want to play more?")
    elif users[message.from_user.id]["attempts"] <= 1:
        users[message.from_user.id]["in_game"] = False
        users[message.from_user.id]["games"] += 1
        await message.answer(f"Wrong. You have no more attempts.\n"
                             f"chosen number was: {users[message.from_user.id]["secret_number"]}")
    else:
        users[message.from_user.id]["attempts"] -= 1
        await message.answer(f"My number is {"bigger" if int(message.text) < users[message.from_user.id]["secret_number"] else "smaller"}")

@dp.message()
async  def process_message(message: Message):
    add_new_user(users, message.from_user.id)
    if users[message.from_user.id]["in_game"]:
        await message.answer(f"We are playing. Please send numbers between 1 and 100")
    else:
        await message.answer(f"Let's play the game")


if __name__ == "__main__":
    dp.run_polling(bot)