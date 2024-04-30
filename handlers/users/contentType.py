from aiogram import types
from aiogram.dispatcher import filters
from aiogram.types import ReplyKeyboardRemove, ContentType, Message
from keyboards.default.menuKeyboard import menu
from loader import dp, bot



from loader import dp
user_choices = {}
# IsSenderContact
@dp.message_handler(content_types='contact', is_sender_contact=True)
# @dp.message_handler(filters.IsSenderContact(True), content_types='contact')
async def sender_contact_example(msg: types.Message):
    user_id = msg.from_user.id
    user_name = msg.from_user.full_name
    user_phone = msg.contact
    #
    await msg.answer(f"Rahmat, <b> {msg.from_user.full_name} </b>sizning kontaktingiz qabul qilindi."
                     f"\n{msg.from_user.full_name} sizdan o'zingiz ishlaydigan xududiy bog'lamaning "
                     f"obektlarinigina taxrir qilishingiz yoki yangilashingizni so'raymiz. "
                     f"Iltimos ma'lumotlarni to'ldirishda ularning to'g'riligiga e'tiborli bo'ling! "
                     f"Barcha xarakatlar log faylga yig'ilib boradi. Raxmat! ", reply_markup=menu)
