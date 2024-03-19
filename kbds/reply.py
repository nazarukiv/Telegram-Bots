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


def get_keyboard(
        *btns: str,
        placeholder: str = None,
        request_contact: int = None,
        request_location: int = None,
        sizes: tuple[int] = (2,),
):
    '''
    Parameters request_contact and request_location must be as indexes of btns args for buttons you need.
    Example:
    get_keyboard(
            "Menu",
            "About our store",
            "Options of payment",
            "Options of delivery",
            "Send phone number"
            placeholder="What areyou interested in?",
            request_contact=4,
            sizes=(2, 2, 1)
        )
    '''
    keyboard = ReplyKeyboardBuilder()

    for index, text in enumerate(btns, start=0):

        if request_contact and request_contact == index:
            keyboard.add(KeyboardButton(text=text, request_contact=True))

        elif request_location and request_location == index:
            keyboard.add(KeyboardButton(text=text, request_location=True))
        else:

            keyboard.add(KeyboardButton(text=text))

    return keyboard.adjust(*sizes).as_markup(
        resize_keyboard=True, input_field_placeholder=placeholder)
