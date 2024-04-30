from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

contactButton = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='📱Contact', request_contact=True),
        ],
    ],
    resize_keyboard=True
)