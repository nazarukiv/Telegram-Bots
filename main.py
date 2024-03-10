import hashlib
from aiogram import Bot, Dispatcher, types, F, MagicFilter
from aiogram.dispatcher import router
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineQuery
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.filters import Command
import asyncio
from aiogram.types import InlineQuery, InputTextMessageContent, InlineQueryResultArticle
from aiogram.fsm.context import FSMContext


TOKEN_API = "6752406818:AAFWkKn_yVUAMJCPTc4dL4tIc_jsnO17o4g"  # Token to verify Telegram API

bot = Bot(TOKEN_API)
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


class ProfileStatesGroup(StatesGroup):
    photo = State()
    name =  State()
    age = State()
    description = State()

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("Welcome to My Bot! Type /create to start", reply_markup=keyboard)

@dp.message(Command("create"))
async def cmd_create(message: types.Message, state: FSMContext):
    await message.answer("Let's create your profile! Please, send me your photo.")
    await state.set_state(ProfileStatesGroup.photo)  # corrected way to set state

@dp.message()
async def load_photo(message: types.Message, state: FSMContext):
    if message.photo:
        photo_id = message.photo[0].file_id
        await state.update_data(photo=photo_id)
        await state.set_state(ProfileStatesGroup.photo)  # corrected way to set state
        await message.answer("Great! Now, please send me your name.")


@dp.message()
async def load_name(message: types.Message, state: FSMContext):
    if message.name:
        name = message.text
        await state.update_data(name_id=name)
        await state.set_state(ProfileStatesGroup.name)  # corrected way to set state
        await message.answer("Great! Now, please send me your age.")


@dp.message()
async def load_age(message: types.Message, state: FSMContext):
    await state.update_data(age=message.text)
    await state.set_state(ProfileStatesGroup.description)
    await message.answer("Great, now tell me something about yourself.")


@dp.message()
async def load_description(message: types.Message, state: FSMContext):
    await state.update_data(description=message.text)
    user_data = await state.get_data()

    # Construct the profile summary
    profile_summary = (
        f"Profile Summary:\n"
        f"Photo ID: {user_data.get('photo')}\n"
        f"Name: {user_data.get('name')}\n"
        f"Age: {user_data.get('age')}\n"
        f"Description: {user_data.get('description')}"
    )

    await message.answer(profile_summary)
    await state.finish()

async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
