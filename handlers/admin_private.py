from aiogram import F, Router, types
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from sqlalchemy.ext.asyncio import AsyncSession

from filters.chat_types import ChatTypeFilter, IsAdmin
from kbds.reply import get_keyboard
from database.orm_query import orm_add_product

admin_router = Router()
admin_router.message.filter(ChatTypeFilter(["private"]), IsAdmin())


ADMIN_KB = get_keyboard(
    "Add products",
    "Change product",
    "Delete product",
    "Just check",
    placeholder="Choose what you want to do.",
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
class AddProduct(StatesGroup):
    name = State()
    description = State()
    price = State()
    image = State()

    texts = {
        'AddProduct:name': 'Write down name again',
        'AddProduct:description': 'Write down description again',
        'AddProduct:price': 'Write down price again',
        'AddProduct:image': "That's last step, then ...",

    }



@admin_router.message(StateFilter(None), F.text == "Add products")
async def add_product(message: types.Message, state: FSMContext):
    await message.answer(
        "Write down name of product", reply_markup=types.ReplyKeyboardRemove()
    )
    await state.set_state(AddProduct.name)

@admin_router.message(Command("Cancel"))
@admin_router.message(F.text.casefold() == "cancel")
async def cancel_handler(message: types.Message, state: FSMContext) -> None:
    current_state = await state.get_state()
    if current_state is None:
        return

    await state.set_state(None)
    await message.answer("Actions canceled", reply_markup=ADMIN_KB)

@admin_router.message(StateFilter('*'), Command("Back"))
@admin_router.message(StateFilter('*'), F.text.casefold() == "back")
async def cancel_handler(message: types.Message, state: FSMContext) -> None:
    current_state = await state.get_state()

    if current_state == AddProduct.name.state:
        await message.answer("Next step is unavailable, or write down name of product or write cancel ")
        return

    previous = None
    for step in AddProduct.__all_states__:
        if step.state == current_state:
            await state.set_state(previous.state)
            await message.answer(f"Cool, you came back to the previous step\n{AddProduct.texts[previous.state]}")
            return
        previous = step

@admin_router.message(AddProduct.name ,F.text)
async def add_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("Write down description of product")
    await state.set_state(AddProduct.description)

@admin_router.message(AddProduct.description, F.text)
async def add_description(message: types.Message, state: FSMContext):
    await state.update_data(description=message.text)
    await message.answer("Write down price of product")
    await state.set_state(AddProduct.price)


@admin_router.message(AddProduct.price, F.text)
async def add_price(message: types.Message, state: FSMContext):
    await state.update_data(price=message.text)
    await message.answer("Upload photo of product")
    await state.set_state(AddProduct.image)


@admin_router.message(AddProduct.image, F.photo)
async def add_image(message: types.Message, state: FSMContext, session: AsyncSession):
    await state.update_data(image=message.photo[-1].file_id)  # Update 'image' key
    await message.answer("Product was added", reply_markup=ADMIN_KB)
    data = await state.get_data()
    try:
        await orm_add_product(session, data)
        await message.answer("Product was added!", reply_markup=ADMIN_KB)
        await state.clear()

    except Exception as e:
        await message.answer(f"Error: \n{str(e)}\n", reply_markup=ADMIN_KB)
    await state.clear()
