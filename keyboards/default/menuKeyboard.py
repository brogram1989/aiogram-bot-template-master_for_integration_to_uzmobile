from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='👷‍♂️ish'),
            KeyboardButton(text='📊statistika'),
        ],
    ],
    resize_keyboard=True
)