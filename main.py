import os
import asyncio
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton, \
    BotCommandScopeAllPrivateChats
from aiogram.filters import Command, CommandStart
from dotenv import find_dotenv, load_dotenv
from common.bot_cmds_list import private
from handlers.user_group import user_group_router


load_dotenv(find_dotenv())

ALLOWED_UPDATES = ['message, edited_message']

bot = Bot(token=os.getenv("TOKEN"), default=DefaultBotProperties(parse_mode=ParseMode.HTML))
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


async def main():
    from handlers.user_private import user_private_router
    dp.include_router(user_private_router)
    dp.include_router(user_group_router)
    #await bot.set_my_commands(commands=private, scope=BotCommandScopeAllPrivateChats())
    await dp.start_polling(bot, allowed_updates=ALLOWED_UPDATES)


if __name__ == '__main__':
    asyncio.run(main())
