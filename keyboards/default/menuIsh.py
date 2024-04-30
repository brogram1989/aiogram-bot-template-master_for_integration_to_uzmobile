from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

menuIsh = ReplyKeyboardMarkup(
    keyboard=[

        [
            KeyboardButton(text='🔎qidirish'),
        ],
        [
            KeyboardButton(text='⚙️jarayonda'),
        ],
        [
            KeyboardButton(text='🔙bosh menuga qaytish'),
        ],
    ],
    resize_keyboard=True
)


menuYukla = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='⬆️ yangi fayli serverga yuklash'),
        ],
        [
            KeyboardButton(text='⬇️ serverdan faylni yuklab olish'),
        ],
    ],
    resize_keyboard=True
)