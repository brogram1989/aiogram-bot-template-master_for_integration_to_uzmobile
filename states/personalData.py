from aiogram.dispatcher.filters.state import StatesGroup, State

class PersonalData(StatesGroup):
    fullName = State()
    phoneNum = State()
class AdminCommands(StatesGroup):
    user_id = State()
    del_user = State()
    set_admin =State()
    del_admin = State()

class FindId(StatesGroup):
    send_file = State() #faylni serverga yuborish stati
    take_file = State() #faylni serverdan qabul qilib olish stati
    search_comand = State() #qidirishni bosganda ishga tushadigan state
    site_id = State() #saytni qidiryotganda ishga tushadigan state
    about_site = State() #sayt xaqida ma'lumot beradigan state
    comment = State() #biror bir sayt uchun komment yangilaydigan state
    time_shift = State() #biror oraliqda ishga tushganlarni aniqlashtirish uchun state