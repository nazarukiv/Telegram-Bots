from aiogram import Dispatcher, types, Router, F
from aiogram.filters import Command, CommandStart, or_f
from main import keyboard
from filters.chat_types import ChatTypeFilter
from kbds import reply


user_private_router = Router()
user_private_router.message.filter(ChatTypeFilter(['private']))

@user_private_router.message(CommandStart())
async def cmd_start(message: types.Message):
    await message.answer("Welcome to My Bot! I'm a virtual bot , that will help you.",
                         reply_markup=reply.start_kb)


@user_private_router.message(or_f(Command("menu"), (F.text == "menu")))
async def menu_cmd(message: types.Message):
    await message.answer("Here is menu:", reply_markup=reply.del_kbd)

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


@user_private_router.message(F.contact)
async def get_contact(message: types.Message):
    await message.answer(f"Number was received")
    await message.answer(str(message.contact))


@user_private_router.message(F.location)
async def get_contact(message: types.Message):
    await message.answer(f"Location was received")
    await message.answer(str(message.location))

@user_private_router.message(Command("location"))
async def get_contact(message: types.Message):
    await message.answer(f"Location was received", reply_markup=reply.test_kb)









