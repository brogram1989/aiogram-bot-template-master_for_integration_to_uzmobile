import sqlite3

from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from keyboards.default.contact import contactButton
from data.config import ADMINS
from loader import dp, bot #, db


@dp.message_handler(commands='start')
@dp.message_handler(text="/start")
@dp.message_handler(CommandStart())
@dp.edited_message_handler(CommandStart())
async def bot_start(message: types.Message):
    await message.answer(f"Assalomu alaykum, {message.from_user.full_name}!")
    await message.answer("Iltimos kontaktingizni yuboring", reply_markup=contactButton)
    name = message.from_user.full_name
    # # foydalanuvchini bazaga qo'shamiz
    # try:
    #     db.add_user(id=message.from_user.id,
    #                 name=name)
    # except sqlite3.IntegrityError as err:
    #     await bot.send_message(chat_id=ADMINS[0], text=err)
    # count = db.count_users()[0]
    # await message.answer("Xush kelibsiz!")
    # #adminga xabar beramiz
    # msg = f"{message.from_user.full_name} bazaga qo'shildi.\nBazada {count} ta foydalanuvchi bor."
    # await bot.send_message(chat_id=ADMINS[0], text=msg)
