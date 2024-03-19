from aiogram import F, Router, types
from aiogram.filters import Command

from filters.chat_types import ChatTypeFilter, IsAdmin
from kbds.reply import get_keyboard


admin_router = Router()
admin_router.message.filter(ChatTypeFilter(["private"]), IsAdmin())


ADMIN_KB = get_keyboard(
    "Добавить товар",
    "Изменить товар",
    "Удалить товар",
    "Я так, просто посмотреть зашел",
    placeholder="Выберите действие",
    sizes=(2, 1, 1),
)


@admin_router.message(Command("admin"))
async def add_product(message: types.Message):
    await message.answer("What do you want to do?", reply_markup=ADMIN_KB)


@admin_router.message(F.text == "Just check")
async def starring_at_product(message: types.Message):
    await message.answer("OK, here is list of your products")


@admin_router.message(F.text == "Change product")
async def change_product(message: types.Message):
    await message.answer("OK, here is list of your products")


@admin_router.message(F.text == "Delete product")
async def delete_product(message: types.Message):
    await message.answer("Choose product and delete")


#For FSM

@admin_router.message(F.text == "Add products")
async def add_product(message: types.Message):
    await message.answer(
        "Write down name of product", reply_markup=types.ReplyKeyboardRemove()
    )


@admin_router.message(Command("Cancel"))
@admin_router.message(F.text.casefold() == "Cancel")
async def cancel_handler(message: types.Message) -> None:
    await message.answer("Actons canceled", reply_markup=ADMIN_KB)


@admin_router.message(Command("Back"))
@admin_router.message(F.text.casefold() == "Back")
async def cancel_handler(message: types.Message) -> None:
    await message.answer(f"OK, we comeback to last step")


@admin_router.message(F.text)
async def add_name(message: types.Message):
    await message.answer("Write down description of product")


@admin_router.message(F.text)
async def add_description(message: types.Message):
    await message.answer("Write down price of product")


@admin_router.message(F.text)
async def add_price(message: types.Message):
    await message.answer("Upload photo of product")


@admin_router.message(F.photo)
async def add_image(message: types.Message):
    await message.answer("Product was added", reply_markup=ADMIN_KB)