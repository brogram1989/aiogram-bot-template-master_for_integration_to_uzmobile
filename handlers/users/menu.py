from aiogram import types

from aiogram.dispatcher.filters import Command, Text
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from keyboards.default.menuKeyboard import menu
from keyboards.default.menuStat import menuStat
from keyboards.default.menuIsh import menuIsh
from keyboards.default.menuYukla import menuYukla
from loader import dp, bot
from handlers.users.excel_handler import excel_data



#menu komandasi uchun menu
@dp.message_handler(Command("menu"))
@dp.message_handler(text="🔙bosh menuga qaytish")
@dp.message_handler(text="menu")
async def show_menu(message:Message):
    await message.answer("Menuni tanglang", reply_markup=menu)

@dp.callback_query_handler(text="back_to_menu")
async def back_to_menu(call: types.CallbackQuery):
    await call.message.answer("Menuni tanglang", reply_markup=menu)


#ish komandasi uchun menu
@dp.message_handler(text="👷‍♂️ish")
async def ish_menu(message:Message):
    await message.answer("siz ishchi bo'limdasiz", reply_markup=menuIsh)


#yukla komandasi uchun menu
@dp.message_handler(text="/yukla")
@dp.message_handler(text="yukla")
async def yukla_menu(message:Message):
    await message.answer("siz fayllarni yuklash bo'limidasiz", reply_markup=menuYukla)

#statistika bo'limi uchun handler
@dp.message_handler(text="📊statistika")
async def statistika_menu(message:Message):
    await message.answer("siz statistika bo'limidasiz", reply_markup=menuStat)


