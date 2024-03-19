from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, KeyboardButtonPollType
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

start_kb2.adjust(2, 1, 1)


start_kb3 = ReplyKeyboardBuilder()
start_kb3.attach(start_kb2) # will add the buttons from keyboard 2
start_kb3.row(KeyboardButton(text="Leave a review"),) #will add this button to new row
start_kb3.adjust(2, 1, 1) #rows structure


test_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Menu", request_poll=KeyboardButtonPollType()),
        ],
        {
            KeyboardButton(text="Send your number📱", request_contact=True),
            KeyboardButton(text="Send your location🗺", request_location=True)
        }
    ],
    resize_keyboard=True,
)