from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram.utils.keyboard import ReplyKeyboardBuilder

start_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Menu"),
            KeyboardButton(text="About our store"),
        ],
        {
            KeyboardButton(text="Options of delivery"),
            KeyboardButton(text="Options of payment")
        }
    ],
    resize_keyboard=True,
    input_field_placeholder="What are you interested in?"
)


del_kbd = ReplyKeyboardRemove() # remove keyboard after pressing /menu


#second options to add keyboards.
start_kb2 = ReplyKeyboardBuilder()
start_kb2.add(
    KeyboardButton(text="Menu"),
    KeyboardButton(text="About our store"),
    KeyboardButton(text="Options of delivery"),
    KeyboardButton(text="Options of payment")
)

start_kb2.adjust(2,2)
