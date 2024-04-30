#foydalanuvchilardan ma'lumotlarni qabul qiladigan handler

from aiogram import  types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command

from loader import dp
from states.personalData import PersonalData

@dp.message_handler(Command('anketa'))
async def enter_test(message: types.Message):
    await message.answer("To`liq ismingizni kiriting")
    # fullName statega o'tish
    await PersonalData.fullName.set()

@dp.message_handler(state=PersonalData.fullName)
async def answer_fullname(message: types.Message, state:FSMContext):
    fullname = message.text
    await state.update_data(
        {'name':fullname}
    )
    await message.answer("Telefon raqamingizni kiriting")
    # phone statega o'tish
    await PersonalData.phoneNum.set()

@dp.message_handler(state=PersonalData.phoneNum)
async def answer_phone(message: types.Message, state:FSMContext):
    phone = message.text
    await state.update_data(
        {'phone':phone}
    )

    #ma'lumotlarni qaytadan o'qiymiz
    data = await state.get_data()
    name = data.get('name')
    phone = data.get('phone')

    msg = "quyidagi ma'lumotlar qabul qilindi: \n"
    msg += f"ismingiz - {name}\n"
    msg += f"raqamingiz - {phone}\n"
    await message.answer(msg)
    # foydalanuvchini statedan chiqazib yuborish
    await state.finish()



