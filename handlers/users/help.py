from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandHelp, CommandPrivacy, CommandSettings

from loader import dp

@dp.message_handler(CommandSettings())
async def bot_help(message: types.Message):
    text = ("Bot sozlamalari")
    await message.answer(text)

@dp.message_handler(CommandHelp())
async def bot_help(message: types.Message):
    text = ("Buyruqlar: ",
            "/start - Botni ishga tushirish",
            "/menu - botning menu bo'limini",
            "/qidir - biror obektni id yoki nomi bo'yicha qidirish"
            "/yukla - ishchi faylini yuklash uchun buyruq(adminlar uchun)",
            "/help - Yordam",
            )
    
    await message.answer("\n".join(text))
   