from aiogram import types
from aiogram.dispatcher.filters import Command
from loader import dp
from data.config import ADMINS, USERS
from aiogram.types import ContentTypes, ReplyKeyboardRemove, Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from states.personalData import AdminCommands
from aiogram.dispatcher import FSMContext


@dp.message_handler(Command("admin"))
async def admin_comands(message: types.Message):
    admin_keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="➕👤 foydalanuvchi qo'shish", callback_data='add_user'),
            ],
            [
                InlineKeyboardButton(text="👥📝foydalanuvchilar ro'yxati", callback_data='list_users'),
            ],
            [
                InlineKeyboardButton(text="🪓👤foydalanuvchini o'chirish", callback_data='del_user'),
            ],
            [
                InlineKeyboardButton(text="✅🥷foydalanuvchini admin qilish", callback_data='set_admin'),
            ],
            [
                InlineKeyboardButton(text="❌🥷 adminlikdan chiqazish", callback_data='del_admin'),
            ],
        ],
    )
    await message.answer("Kerakli bo'limni tanlang!",
                         reply_markup=admin_keyboard)

# Check if the user is an admin

def is_admin(user_id: int):
    return user_id in ADMINS

def is_user(user_id: int):
    return user_id in USERS
def add_user(user_id: int ):
    if user_id not in USERS:
        USERS.append(user_id)
        return "User muvaffaqqiyatli qo'shildi!"
    else:
        return "Bu id dagi user mavjud!"

def del_user(user_id: int ):
    if user_id in USERS:
        USERS.remove(user_id)
        return "User muvaffaqqiyatli o'chirildi!"
    else:
        return "Bu id dagi user mavjud emas!"

def set_admin(user_id: int ):
    if user_id not in ADMINS:
        ADMINS.append(user_id)
        return "User muvaffaqqiyatli qo'shildi!"
    else:
        return "Bu id dagi user mavjud!"

def remove_admin(user_id: int ):
    if user_id in ADMINS:
        ADMINS.remove(user_id)
        return "Admin muvaffaqqiyatli o'chirildi!"
    else:
        return "Bu id dagi admin mavjud emas!"

# Handling callback queries for admin commands
@dp.callback_query_handler(lambda callback_query: callback_query.data.startswith("add_user"))
async def admin_check(callback_query: types.CallbackQuery):
    if is_admin(callback_query.from_user.id):
        await callback_query.answer("Yangi foydalanuvchini qo'shing")
        await callback_query.message.answer("Yangi foydalanuvchi qo'shish uchun uning ID nomerini kirgazing. \n"
                                    "Foydalanuvchi 🆔 sini aniqlash uchun https://t.me/username_to_id_bot dan foydalanishingiz mumkun")
        await callback_query.message.answer("<code>🆔 faqatgina raqamlardan iborat ketma ketligdagi son</code>")
        await AdminCommands.user_id.set()
    else:
        await callback_query.answer("Siz admin emasiz")


#admin kirgizadigan useridni USERS listga yozish uchun handler

@dp.message_handler(state=AdminCommands.user_id)
async def new_users_id(message: types.Message, state:FSMContext):
    try:
        # Get the comment from the message
        new_user = message.text
        new_user = int(new_user)
        add_user(new_user)
        await message.answer(f"siz id={new_user} foydalanuvchini bazaga kiritdingiz!\nBazada {len(USERS)} ta foydalanuvchi bor")
        # Finish the state
        await state.finish()
    except Exception as e:
        await message.reply(f"❌❓Xatolik yuzaga keldi: <b>{str(e)}</b>\n"
                            f"qaytadan urinib ko'ring!")
        await state.finish()

@dp.callback_query_handler(lambda callback_query: callback_query.data.startswith("list_users"))
async def list_users(callback_query: types.CallbackQuery):
    if is_admin(callback_query.from_user.id):
        # Your logic to delete a user here
        await callback_query.message.answer(f"Bazada {len(USERS)} ta 👤 foydalanuvchi bor.\nFoydalanuvchilar ro'yxati\n"
                                            f"{USERS}")
        await callback_query.message.answer(f"Bazada {len(ADMINS)} ta 🥷 admin bor.\nAdminlar ro'yxati\n{ADMINS}")
    else:
        await callback_query.answer("Siz admin emasiz")



@dp.callback_query_handler(lambda callback_query: callback_query.data.startswith("del_user"))
async def delete_user(callback_query: types.CallbackQuery):
    if is_admin(callback_query.from_user.id):
        # Your logic to delete a user here
        await callback_query.message.answer("Foydalanuvchini o'chirish, uning 🆔 sini kiriting. \n"
                                            "<code>🆔 faqatgina raqamlardan iborat ketma ketligdagi son</code>")
        await AdminCommands.del_user.set()
    else:
        await callback_query.answer("Siz admin emasiz")



#admin kirgizadigan useridni USERS listdan o'chirish uchun handler

@dp.message_handler(state=AdminCommands.del_user)
async def del_users(message: types.Message, state:FSMContext):
    try:
        # Get the comment from the message
        user_id = message.text
        user_id = int(user_id)
        del_user(user_id)
        await message.answer(f"id={user_id} foydalanuvchi bazadan o'chirildi!\nBazada {len(USERS)} ta foydalanuvchi qoldi!")
        # Finish the state
        await state.finish()
    except Exception as e:
        await message.reply(f"❌❓Xatolik yuzaga keldi: <b>{str(e)}</b>\n"
                            f"qaytadan urinib ko'ring!")
        await state.finish()


@dp.callback_query_handler(lambda callback_query: callback_query.data.startswith("set_admin"))
async def set_new_admin(callback_query: types.CallbackQuery):
    if is_admin(callback_query.from_user.id):
        # Your logic to set a user as admin here
        await callback_query.message.answer("Foydalanuvchini admin qilish uchun, uning 🆔 sini kiriting. \n"
                                    "<code>🆔 faqatgina raqamlardan iborat ketma ketligdagi son</code>")
        await AdminCommands.set_admin.set()
    else:
        await callback_query.answer("Siz admin emasiz")

@dp.message_handler(state=AdminCommands.set_admin)
async def new_admin(message: types.Message, state:FSMContext):
    try:
        # Get the comment from the message
        admin = message.text
        admin = int(admin)
        add_user(admin)
        set_admin(admin)
        await message.answer(f"siz id={admin} foydalanuvchini admin qilib belgiladingiz!\nBazada {len(ADMINS)} ta admin bor")
        # Finish the state
        await state.finish()
    except Exception as e:
        await message.reply(f"❌❓Xatolik yuzaga keldi: <b>{str(e)}</b>\n"
                            f"qaytadan urinib ko'ring!")
        await state.finish()

@dp.callback_query_handler(lambda callback_query: callback_query.data.startswith("del_admin"))
async def delete_admin(callback_query: types.CallbackQuery):
    if is_admin(callback_query.from_user.id):
        # Your logic to remove admin privileges from a user here
        await callback_query.answer("userni adminlikdan chiqarish")
        await callback_query.message.answer("Foydalanuvchini adminlar ro'yxatidan o'chirish uchun, uning 🆔 sini kiriting. \n"
                                            "<code>🆔 faqatgina raqamlardan iborat ketma ketligdagi son</code>")
        await AdminCommands.del_admin.set()
    else:
        await callback_query.answer("Siz admin emasiz")


#admin kirgizadigan useridni ADMINS listdan o'chirish uchun handler

@dp.message_handler(state=AdminCommands.del_admin)
async def del_admin(message: types.Message, state:FSMContext):
    try:
        # Get the comment from the message
        user_id = message.text
        user_id = int(user_id)
        remove_admin(user_id)
        await message.answer(f"id={user_id} admin bazadan o'chirildi!\nBazada {len(ADMINS)} ta admin qoldi!")
        # Finish the state
        await state.finish()
    except Exception as e:
        await message.reply(f"❌❓Xatolik yuzaga keldi: <b>{str(e)}</b>\n"
                            f"qaytadan urinib ko'ring!")
        await state.finish()