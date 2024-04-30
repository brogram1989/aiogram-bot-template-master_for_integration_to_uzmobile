from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

menuYukla = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='⬆️ yangi faylni serverga yuklash'),
        ],
        [
            KeyboardButton(text='⬇️ serverdan faylni yuklab olish'),
        ],
    ],
    resize_keyboard=True
)