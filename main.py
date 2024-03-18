import hashlib
import os

from aiogram import Bot, Dispatcher, types, F, MagicFilter
from aiogram.dispatcher import router
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineQuery
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.filters import Command, CommandStart
import asyncio
from aiogram.types import InlineQuery, InputTextMessageContent, InlineQueryResultArticle
from aiogram.fsm.context import FSMContext
from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())

bot = Bot(token=os.getenv("TOKEN"))
dp = Dispatcher()

inl = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text='Binance', url="https://www.binance.com/en"),
        InlineKeyboardButton(text='ByBit', url="https://www.bybit.com/en/")
    ],
])

keyboard = ReplyKeyboardMarkup(
   keyboard=[
       [KeyboardButton(text="/create")],
   ],
   resize_keyboard=True,
   one_time_keyboard=True
)


HELP_COMMAND = """
<b>/help</b>-<em>list of commands</em>
<b>/start</b>-<em>start the bot</em>
"""

print("Test")


@dp.message(CommandStart())
async def cmd_start(message: types.Message):
    await message.answer("Welcome to My Bot! Type /create to start", reply_markup=keyboard)


@dp.message()
async def echo(message: types.Message):
    await message.answer(message.text)




async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
