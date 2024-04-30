from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

menuStat = ReplyKeyboardMarkup(
    keyboard=[

        [
            KeyboardButton(text='📆bugungi ishga tushish rejasi'),
            KeyboardButton(text="📆vaqt oralig'ida ishga tushganlar"),
        ],
        [
            KeyboardButton(text='⚙️bugungi bajarilgan ishlar'),
            KeyboardButton(text='⚙️jarayonda'),
        ],
        [
            KeyboardButton(text='🔙bosh menuga qaytish'),
        ],
    ],
    resize_keyboard=True
)