import hashlib
from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineQuery
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.filters import Command
import asyncio
from aiogram.types import InlineQuery, InputTextMessageContent, InlineQueryResultArticle


TOKEN_API = "6752406818:AAFWkKn_yVUAMJCPTc4dL4tIc_jsnO17o4g"  # Token to verify Telegram API

bot = Bot(TOKEN_API)
dp = Dispatcher()



inl = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text='Binance', url="https://www.binance.com/en"),
        InlineKeyboardButton(text='ByBit', url="https://www.bybit.com/en/")
    ],
])


HELP_COMMAND = """
<b>/help</b>-<em>list of commands</em>
<b>/start</b>-<em>start the bot</em>
"""


@dp.message(Command("start"))
async def cmd_start(message: types.Message) -> None:
    await message.answer(text="<b>Welcome to My Bot!</b>\n\n<i>Explore the world of IT</i>", parse_mode="HTML")
    await message.delete()


async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
