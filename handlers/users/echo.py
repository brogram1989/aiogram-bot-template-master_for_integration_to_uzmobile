from aiogram import types

from loader import dp


# Echo bot
@dp.message_handler(state=None)
async def bot_echo(message: types.Message):
    await message.answer("exo bo'limiga tushdingiz! Bot menudagi buyruqlardan boshqa gaplarizga javob bermaydi!")
