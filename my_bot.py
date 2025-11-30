import os
import requests
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.types import Message, ContentType

load_dotenv()
BOT_TOKEN = os.getenv('BOT_TOKEN')

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

async def process_waifu_command(message: Message):
    waifu_response = requests.get("https://api.waifu.im/search")
    await message.answer_photo(waifu_response.json()['images'][0]["url"])

async def process_start_command(message: Message):
    await message.answer("Hi, I am echo and i have many cats")

async def process_help_command(message: Message):
    await message.answer("Send me anything and I'll repeat after you")

async  def process_message(message: Message):
    try:
        await message.send_copy(chat_id=message.chat.id)
    except TypeError:
        await message.reply(text="TypeError")


if __name__ == "__main__":
    dp.message.register(process_start_command, Command(commands="start"))
    dp.message.register(process_help_command, Command(commands="help"))
    dp.message.register(process_waifu_command, Command(commands="waifu"))
    dp.message.register(process_message)
    dp.run_polling(bot)