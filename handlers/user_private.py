from aiogram import Dispatcher, types, Router, F
from aiogram.filters import Command, CommandStart, or_f
from main import keyboard

user_private_router = Router()

@user_private_router.message(CommandStart())
async def cmd_start(message: types.Message):
    await message.answer("Welcome to My Bot! I'm a virtual bot , that will help you.")


@user_private_router.message(or_f(Command("menu"), (F.text == "menu")))
async def menu_cmd(message: types.Message):
    await message.answer("Here is menu:")

@user_private_router.message(Command("about"))
async def about_cmd(message: types.Message):
    await message.answer("About Us:")

@user_private_router.message(Command("payment"))
async def payment_cmd(message: types.Message):
    await message.answer("Options for payment:")

@user_private_router.message(F.text == "options")
@user_private_router.message(Command("shipping"))
async def ship_cmd(message: types.Message):
    await message.answer("Shipping details and options:")






