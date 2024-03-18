from aiogram import Dispatcher, types, Router
from aiogram.filters import Command, CommandStart
from main import keyboard

user_private_router = Router()

@user_private_router.message(CommandStart())
async def cmd_start(message: types.Message):
    await message.answer("Welcome to My Bot! I'm a virtual bot , that will help you.")

@user_private_router.message(Command("menu"))
async def menu_cmd(message: types.Message):
    await message.answer("Here is menu:")


