from aiogram import types


async def set_default_commands(dp):
    await dp.bot.set_my_commands(
        [
            types.BotCommand("start", "Botni ishga tushurish"),
            types.BotCommand("admin", "botga foydalanuvchilar qo'shish, o'chirish, admin belgilash va foydalanuvchilar ro'yxatini ko'rish"),
            types.BotCommand("menu", "Bot menusi"),
            types.BotCommand("qidir", "ID yoki BS nomi bo'yicha qidirish"),
            types.BotCommand("yukla", "Bot ishchi faylini yuklash(faqat adminlar uchun)"),
            types.BotCommand("help", "Yordam"),
        ]
    )
