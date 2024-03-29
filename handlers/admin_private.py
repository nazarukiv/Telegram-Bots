from aiogram import F, Router, types
from aiogram.filters import Command, StateFilter, or_f
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from sqlalchemy.ext.asyncio import AsyncSession

from filters.chat_types import ChatTypeFilter, IsAdmin
from kbds.inline import get_callback_btns
from kbds.reply import get_keyboard
from database.orm_query import orm_add_product, orm_get_products, orm_delete_product, orm_get_product, \
    orm_update_product

admin_router = Router()
admin_router.message.filter(ChatTypeFilter(["private"]), IsAdmin())


ADMIN_KB = get_keyboard(
    "Add products",
    "Catalog",
    placeholder="Choose what you want to do.",
    sizes=(2,),
)

class AddProduct(StatesGroup):
    name = State()
    description = State()
    price = State()
    image = State()

    product_for_change = None

    texts = {
        'AddProduct:name': 'Write down name again',
        'AddProduct:description': 'Write down description again',
        'AddProduct:price': 'Write down price again',
        'AddProduct:image': "That's last step, then ...",

    }

@admin_router.message(Command("admin"))
async def add_product(message: types.Message):
    await message.answer("What do you want to do?", reply_markup=ADMIN_KB)


@admin_router.message(F.text == "Catalog")
async def starring_at_product(message: types.Message, session: AsyncSession):
    for product in await orm_get_products(session):
        await message.answer_photo(
            product.image,
            caption=f"<strong>{product.name}\
                    </strong>\n{product.description}\nPrice: {round(product.price, 2)}",
            reply_markup=get_callback_btns(
                btns={
                    "Delete": f"delete_{product.id}",
                    "Change": f"change_{product.id}",
                }
            ),
        )
    await message.answer("OK, here is list of products ⏫")


@admin_router.callback_query(F.data.startswith("delete_"))
async def delete_product_callback(callback: types.CallbackQuery, session: AsyncSession):
    product_id = callback.data.split("_")[-1]
    await orm_delete_product(session, int(product_id))

    await callback.answer("Product deleted!")
    await callback.message.answer("Product deleted!")

@admin_router.callback_query(StateFilter(None), F.data.startswith("change_"))
async def change_product_callback(
    callback: types.CallbackQuery, state: FSMContext, session: AsyncSession
):
    product_id = callback.data.split("_")[-1]

    product_for_change = await orm_get_product(session, int(product_id))

    AddProduct.product_for_change = product_for_change

    await callback.answer()
    await callback.message.answer(
        "Write down name of product", reply_markup=types.ReplyKeyboardRemove()
    )
    await state.set_state(AddProduct.name)


# waiting for entering name
@admin_router.message(StateFilter(None), F.text == "Add product")
async def add_product(message: types.Message, state: FSMContext):
    await message.answer(
        "Write down the name of product ", reply_markup=types.ReplyKeyboardRemove()
    )
    await state.set_state(AddProduct.name)


#For FSM
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

# Taking data for state name and then change for description
@admin_router.message(AddProduct.name, or_f(F.text, F.text == "."))
async def add_name(message: types.Message, state: FSMContext):
    if message.text == ".":
        await state.update_data(name=AddProduct.product_for_change.name)
    else:
        if len(message.text) >= 100:
            await message.answer(
                "Name of product shouldn't be more than 100 letters. \n Write down again."
            )
            return

        await state.update_data(name=message.text)
    await message.answer("Write down description of product")
    await state.set_state(AddProduct.description)


# Handler for handle uncorrected inputs for state name
@admin_router.message(AddProduct.name)
async def add_name2(message: types.Message, state: FSMContext):
    await message.answer("You wrote down incorrect value.")


# Taking data for state description and then change state for price
@admin_router.message(AddProduct.description, or_f(F.text, F.text == "."))
async def add_description(message: types.Message, state: FSMContext):
    if message.text == ".":
        await state.update_data(description=AddProduct.product_for_change.description)
    else:
        await state.update_data(description=message.text)
    await message.answer("Write down price of product")
    await state.set_state(AddProduct.price)



@admin_router.message(AddProduct.description)
async def add_description2(message: types.Message, state: FSMContext):
    await message.answer("You wrote down incorrect value, write down description again")



@admin_router.message(AddProduct.price, or_f(F.text, F.text == "."))
async def add_price(message: types.Message, state: FSMContext):
    if message.text == ".":
        await state.update_data(price=AddProduct.product_for_change.price)
    else:
        try:
            float(message.text)
        except ValueError:
            await message.answer("Write down correct price")
            return

        await state.update_data(price=message.text)
    await message.answer("Upload Image")
    await state.set_state(AddProduct.image)



@admin_router.message(AddProduct.price)
async def add_price2(message: types.Message, state: FSMContext):
    await message.answer("You wrote down incorrect value, write down price again")


@admin_router.message(AddProduct.image, or_f(F.photo, F.text == "."))
async def add_image(message: types.Message, state: FSMContext, session: AsyncSession):
    if message.text and message.text == ".":
        await state.update_data(image=AddProduct.product_for_change.image)

    else:
        await state.update_data(image=message.photo[-1].file_id)
    data = await state.get_data()
    try:
        if AddProduct.product_for_change:
            await orm_update_product(session, AddProduct.product_for_change.id, data)
        else:
            await orm_add_product(session, data)
        await message.answer("Product added/changed", reply_markup=ADMIN_KB)
        await state.clear()

    except Exception as e:
        await message.answer(
            f"Error: \n{str(e)}",
            reply_markup=ADMIN_KB,
        )
        await state.clear()

    AddProduct.product_for_change = None


@admin_router.message(AddProduct.image)
async def add_image2(message: types.Message, state: FSMContext):
    await message.answer("Upload image of food")

