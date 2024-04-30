import pandas as pd
import io
from io import BytesIO
from aiogram.types import ContentTypes, ReplyKeyboardRemove, Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram import types
from loader import bot, dp
from states.personalData import FindId
from aiogram.dispatcher import FSMContext
from keyboards.inline.inline_keyboard import InlineKeyboardBuilder, choices
from keyboards.default.menuIsh import menuIsh
from keyboards.default.menuKeyboard import menu
from datetime import date, datetime, timedelta
from .user import is_user, is_admin


#_____________________________________________________________________________________________________________________#

#worksheetni saqlab olish uchun dataframe
excel_data = pd.DataFrame()
# Get today's date
today_date = date.today().strftime("%Y-%m-%d")
# Access the original filename of the uploaded document
original_filename = ''
dict = {
    "supply_eq": "Доставка на объект",
    "fit_eq": "Монтаж в процессе",
    "finish_fit_eq": "Монтаж заверщен",
    "launch_ongoing": "Запуск в процессе",
    "launch_finish": "Запуск",
}

#_____________________________________________________________________________________________________________________#
#faylni serverdan yuklash uchun funksiya
async def download_file(file_id):
    file_info = await bot.get_file(file_id)
    downloaded_file = await bot.download_file(file_info.file_path)

    return BytesIO(downloaded_file.read()), file_info


#faylni serverga yuklash handleri
@dp.message_handler(text="⬆️ yangi faylni serverga yuklash")
async def fayl_yubor(message:Message):
    if is_admin(message.from_user.id):
        await message.answer("📎 tegishli faylni serverga yuklang ", reply_markup=ReplyKeyboardRemove())
        #state belgilaymiz
        await FindId.send_file.set()
    else:
        await message.answer("🚫Siz admin emassiz, fayl yuklolmaysiz!", reply_markup=ReplyKeyboardRemove())
    # Command to handle incoming Excel files
    #ikkinchi usul
    # 3 martta urinishdan so'ng statedan chiqib ketadigan qilish uchun i ni elon qilamiz
soni = 1
xisob = 0
bugun = date.today()
today_date_str = date.today().strftime("%Y-%m-%d")
@dp.message_handler(content_types=ContentTypes.DOCUMENT, state=FindId.send_file)
async def handle_document(message: types.Message, state:FSMContext):
    global excel_data, soni, bugun, today_date_str  # Declare the global variable

    try:
        # Download the Excel file
        file_content, info = await download_file(message.document.file_id)

        # Load the Excel file into a Pandas DataFrame
        excel_data = pd.read_excel(file_content, sheet_name='ZTE_&_HUAWEI', engine='openpyxl')
        #excel_data da data typelarni keyinchalik ishlov uchun belgilab olish 5chi qatordan datetypega o'tkazamiz.
        #chunki obektlar 4chi qatordan boshlanyabdi. 3birinchi qatordan boshlanganda
        #excel_data["Доставка на объект"] = pd.to_datetime(excel_data["Доставка на объект"], errors="coerce").dt.strftime("%Y-%m-%d")
        #bo'lar edi
        excel_data.loc[3:, "Доставка на объект"] = pd.to_datetime(excel_data.loc[3:, "Доставка на объект"],
                                                                  errors="coerce").dt.strftime("%Y-%m-%d")
        excel_data.loc[3:, "Монтаж в процессе"] = pd.to_datetime(excel_data.loc[3:, "Монтаж в процессе"],
                                                                  errors="coerce").dt.strftime("%Y-%m-%d")
        excel_data.loc[3:, "Монтаж заверщен"] = pd.to_datetime(excel_data.loc[3:, "Монтаж заверщен"],
                                                                  errors="coerce").dt.strftime("%Y-%m-%d")
        excel_data.loc[3:, "Запуск в процессе"] = pd.to_datetime(excel_data.loc[3:, "Запуск в процессе"],
                                                                  errors="coerce").dt.strftime("%Y-%m-%d")
        excel_data.loc[3:, "Запуск"] = pd.to_datetime(excel_data.loc[3:, "Запуск"],
                                                                  errors="coerce").dt.strftime("%Y-%m-%d")

        # Process the DataFrame as needed
        # For example, you can use excel_data to read, update, or delete values

        await message.reply(f"\n <b>✅ Excel fayl muvafaqqiyatli yuklandi.</b>")
    except Exception as e:

        await message.reply(f"❌❓Qandaydir xato sodir bo'ldi : <b>{str(e)}</b>\n"
                            f"Iltomos qaytadan fayl yuklab ko'ring!📎\n"
                            f"{soni}-urunish. 3chi urunishdan so'ng xolatdan chiqib ketasiz."
                            )
        if soni == 3:
            await state.finish()
            await message.answer(f"Xolatdan chiqib ketdingiz, kerakli fayl yuklayotganingizga ishonchingiz komilmi?")
        else:
            soni += 1
            # Do not finish the state, allowing the user to try again
            return


    #agar tegishli fayl yuklansa statedan chiqib ketamiz
    await state.finish()

#_____________________________________________________________________________________________________________________#


# Example function that uses excel_data
#qidiruv state ga o'tamiz
@dp.message_handler(commands=['🔎qidirish'])
@dp.message_handler(commands=['qidir'])
@dp.message_handler(text='🔎qidirish')
@dp.message_handler(text='/qidir')
@dp.message_handler(state=FindId.search_comand)
async def show_data(message: types.Message):
    if not is_user(message.from_user.id):
        await message.answer("🚫Siz user emassiz!", reply_markup=ReplyKeyboardRemove())
    else:
        await message.answer("Iltimos qidirmoqchi bo'lgan baza stansiya <b>ID</b>si "
                             "yoki <b>nomi</b>ni kiriting\nmisol uchun"
                             " <code>TSH1375</code> yoki <code>Katta Olmos</code>", reply_markup=ReplyKeyboardRemove())
        # sayt qidirish state belgilaymiz
        await FindId.site_id.set()

@dp.message_handler(state=FindId.site_id)
async def pick_siteid(message: types.Message, state: FSMContext):
    try:
        # Get user information
        find_id = message.text
        user_id = message.from_user.id
        text = message.from_user.mention
        info = message.from_user.values

        # Get xisob value from FSMContext
        data = await state.get_data()
        xisob = data.get("xisob", 0)

        # Update data in FSMContext
        await state.update_data({
            "find_id": find_id,
            "user_id": user_id,
            "text": text,
            "info": info,
            "xisob": xisob  # Ensure xisob is stored in FSMContext
        })

        if excel_data is not None:
            # Perform data operations
            df = excel_data
            df['BTS Name'] = df['BTS Name'].str.upper()
            maska = df['BTSID'].str.contains(find_id.upper(), na=False) | df['BTS Name'].str.contains(find_id.upper(), na=False)
            search_result = df[maska].sort_values(by=['BTSID']).head(10)[['BTSID', 'BTS Name']]
            df['BTS Name'] = df['BTS Name'].str.capitalize()

            if search_result.shape[0] != 0:
                # Handle case when search result is found
                keyboard_builder = InlineKeyboardBuilder()
                for index, row in search_result.iterrows():
                    button_name = row['BTSID'] + '     ' + row['BTS Name'].title()
                    callback_data = 'btsid' + row['BTSID']
                    keyboard_builder.add_button(button_name, callback_data)

                keyboard_builder.add_button("🔎boshqa saytlarni qidirib ko'rish", callback_data='again')
                site_inlinekeyboard = keyboard_builder.create_keyboard()
                await message.answer("Topilgan obektlar\nKerakli BS ni tanlang!\n", reply_markup=site_inlinekeyboard)
            else:
                # Handle case when search result is empty
                xisob += 1  # Increment xisob
                await state.update_data({"xisob": xisob})  # Update xisob in FSMContext
                if xisob >= 3:
                    await message.reply(f"botni ham charchatib yubordingiz akaaa! keyinroq bir urunib ko'ring ! ")
                    await state.finish()
                else:
                    await message.reply(f"Siz kiritayotgan id yoki nomdagi BS ma'lumotlar bazasidan topilmadi, qaytadan urunib ko'ring")

    except Exception as e:
        await message.reply(f" ❌❓Qandaydir xato sodir bo'ldi : <b>{str(e)}</b>\n"
                            f"kerakli fayl yuklanmagan bo'lsa, admin avval faylni yuklashi kerak")
    await state.finish()

# boshqa saytlarni qidirish bosilgan bo'lsa boshiga qaytadi
@dp.callback_query_handler(lambda c: c.data.startswith('again'))
async def btsid_button(callback_query: types.CallbackQuery):
    await callback_query.message.answer(text="Ish bo'yicha menu",reply_markup=menuIsh)

# Define a dictionary to store the user's choice
# user tanlagan sayt bo'yicha ma'lumot chiqazish
user_choices = {}


@dp.callback_query_handler(lambda c: c.data.startswith('btsid'))
async def handle_btsid_button(callback_query: types.CallbackQuery):
    try:
        # Extract the BTSID from the callback data
        bts_id = callback_query.data[5:]


        # Retrieve the corresponding row from the DataFrame
        selected_row = excel_data[excel_data['BTSID'] == bts_id].iloc[0]


        # Extract information from the selected row
        bts_name = selected_row['BTS Name']
        # Add more columns as needed
        bts_address = selected_row['BTS adres']
        bts_status = selected_row['Online\\New sites']
        bts_type = selected_row['Type BTS']
        curent_tec = selected_row['Существующая технология']
        moder_tec = selected_row['Технология после модернизации']
        vendor = selected_row['Vendor']
        phase = selected_row['Contract and PO number']
        supply_eq = selected_row["Доставка на объект"]
        mounting_ongoing = selected_row["Монтаж в процессе"]
        mounting = selected_row["Монтаж заверщен"]
        launch_ongoing = selected_row["Запуск в процессе"]
        launch = selected_row["Запуск"]
        region = selected_row["Region"]
        comment = selected_row["Коментарий"]
        # Location for the 📍 icon
        long = selected_row['Longitude']
        lat = selected_row['Latitude']
        url = f"http://maps.google.com/maps?q={lat},{long}"

        info_about_bs = f"""
Tanlangan BTS bo'yicha ma'lumotlar: \n
1. <b>🆔:</b>  {bts_id}
2. <b>Nomi:</b>  {bts_name}
3. <b>🏘Manzili:</b>    {bts_address}
4. <b>📶online/offline:</b>  {bts_status}
5. <b>BTS turi:</b>   {bts_type}
6. <b>📂mavjud texnologiya:</b>   {curent_tec}
7. <b>🗂modernizatsiyadan keyingi texnologiya:</b>  {moder_tec}
8. <b>🗺region:</b>   {region}
9. <b>vendor:</b>     {vendor} 
10. <b>faza:</b>   {phase}
11. <b>📆 qurilmalar yetkazildi 🚛:</b>  {supply_eq}
12. <b>📆 obekt montaji boshlandi ⚙️🛠:</b>  {mounting_ongoing}
13. <b>📆 obekt montaji tugallandi ✅🛠:</b>   {mounting}
14. <b>📆 zapusk boshlandi ⚙️📶:</b>   {launch_ongoing}
15. <b>📆 zapusk bo'ldi ✅📶:</b>  {launch}
16. <b> obekt bo'yicha izoh :</b>  {comment}
<a href="http://maps.google.com/maps?q={lat},{long}">📍lokatsiya</a>

  """

        # Respond to the button press
        await bot.answer_callback_query(callback_query.id,
                                        f"{callback_query.from_user.first_name}, siz : {bts_id} - {bts_name} ni tanladingiz")

        user_id = callback_query.from_user.id
        user_name = callback_query.from_user.first_name


        # Update user_choices dictionary with the selected options
        if user_id not in user_choices:
            user_choices[user_id] = {"user_name": user_name, bts_id: {}}
        else:
            user_choices[user_id]["user_name"] = user_name
            if bts_id not in user_choices[user_id]:
                user_choices[user_id][bts_id] = {}

        if is_admin(callback_query.from_user.id):
            SiteEdit = InlineKeyboardMarkup(
                inline_keyboard=[
                    [
                        InlineKeyboardButton(text="🚚qurilma yetkazildi", callback_data=f'supply_eq_btsid{bts_id}'),
                    ],
                    [
                        InlineKeyboardButton(text="🅿️🛠montaj boshlandi", callback_data=f'fit_eq_btsid{bts_id}'),
                        InlineKeyboardButton(text="✅🛠montaj tugallandi", callback_data=f'finish_fit_eq_btsid{bts_id}'),
                    ],
                    [
                        InlineKeyboardButton(text="🅿️⚙️zapusk boshlandi", callback_data=f'launch_ongoing_btsid{bts_id}'),
                        InlineKeyboardButton(text="✅📶zapusk bo'ldi", callback_data=f'launch_finish_btsid{bts_id}'),
                    ],
                    [
                        InlineKeyboardButton(text="📋izoh yozish", callback_data=f'comment_btsid{bts_id}'),
                    ],
                    [
                        InlineKeyboardButton(text="✅📝o'zgarishlarni faylga saqlash", callback_data=f'apply_changes_btsid{bts_id}'),
                    ],
                    [
                        InlineKeyboardButton(text="🏠bosh menuga qaytish", callback_data='back_to_menu'),
                    ],
                ],
            )
        else:
            SiteEdit = InlineKeyboardMarkup(
                inline_keyboard=[
                    [
                        InlineKeyboardButton(text="🚚qurilma yetkazildi", callback_data=f'supply_eq_btsid{bts_id}'),
                    ],
                    [
                        InlineKeyboardButton(text="🅿️🛠montaj boshlandi", callback_data=f'fit_eq_btsid{bts_id}'),
                        InlineKeyboardButton(text="✅🛠montaj tugallandi", callback_data=f'finish_fit_eq_btsid{bts_id}'),
                    ],
                    [
                        InlineKeyboardButton(text="🅿️⚙️zapusk boshlandi", callback_data=f'launch_ongoing_btsid{bts_id}'),
                    ],
                    [
                        InlineKeyboardButton(text="📋izoh yozish", callback_data=f'comment_btsid{bts_id}'),
                    ],
                    [
                        InlineKeyboardButton(text="✅📝o'zgarishlarni faylga saqlash", callback_data=f'apply_changes_btsid{bts_id}'),
                    ],
                    [
                        InlineKeyboardButton(text="🏠bosh menuga qaytish", callback_data='back_to_menu'),
                    ],
                ],
            )

        await callback_query.message.answer(f"{info_about_bs}\n", reply_markup=None)
        await callback_query.message.answer(f"<code>{bts_id}</code> bo'yicha bugungi rejani quyidagi tugmalar orqali belgilang."
                                            f"<b>Bir vaqtda bir nechta variant tanlashingiz mumkun.</b>"
                                            f"agar, biror bo'limni ortiqcha belgilab qo'ygan bo'lsangiz, o'sha bo'limni "
                                            f"yana qayta bossangiz belgilanganlardan chiqadi!"
                                            f"\n Sayt bo'yicha rejalarni belgilab bo'lganingizdan so'ng,\n"
                                            f"<code>✅📝o'zgarishlarni faylga saqlash</code>ni bosing\n"
                                            f"Barcha rejalarni kiritganingizdan keyin \n"
                                            f"<code>🏠bosh menuga qaytish</code> tugmasi orqali\n"
                                            f"bosh menuga qaytishingiz mumkun"
                                            f"\nIzoh qismi bo'lsa batafsil izoh yozing. (EP, Transport yoki boshqa "
                                            f"bo'yicha muammolar) \n"
                                            f"<b> Eslatma: Izoh qismi alohida yoziladi, izoh uchun <code>✅📝o'zgarishlarni faylga saqlash</code>"
                                            f"ni bosish shart emas!</b>", reply_markup=SiteEdit)

        # Remove the inline keyboard by editing the message
        await bot.edit_message_reply_markup(chat_id=callback_query.message.chat.id,
                                            message_id=callback_query.message.message_id,
                                            reply_markup=None)

    except IndexError:
        # Handle the case where the selected BTSID is not found in the DataFrame
        await bot.answer_callback_query(callback_query.id, "Error: Selected BTSID not found.")


# Define handlers for option selection and applying changes

@dp.callback_query_handler(lambda c: any(c.data.startswith(option.split("_btsid")[0]) for option in choices))
async def handle_option_selection(call: types.CallbackQuery):
    try:
        user_id = call.from_user.id
        user_name = call.from_user.first_name
        bts_id = call.data.split('_btsid')[1]
        option = call.data.split('_btsid')[0]
        #option variantlarini dict ga yozib olamiz


        # Update user_choices dictionary with the selected options
        if user_id not in user_choices:
            user_choices[user_id] = {"user_name": user_name, bts_id: {}}

        if option not in user_choices[user_id][bts_id]:
            # qaysi option tanlangan bo'lsa o'sha o'ptionga bugungi kunni yozish
            user_choices[user_id][bts_id][option] = today_date
            # Update the DataFrame based on the selected option
            # qaysi option tanlangan bo'lsa o'sha o'ptionga bugungi kunni yozish faqat DataFrame uchun endi
            excel_data.loc[excel_data["BTSID"] == bts_id, dict[option]] = today_date
            #example option==""Запуск""
            #excel_data.loc[excel_data["BTSID"]==bts_id,"Запуск"]=today_date
        else:
            # Toggle the selection state of the option
            if option in user_choices[user_id][bts_id]:
                # optionni user_choises lug'atidan o'chirish
                del user_choices[user_id][bts_id][option]
                # qaysi option olingan  bo'lsa o'sha o'ptiondagi datani o'chirish DataFrame uchun endi
                excel_data.loc[excel_data["BTSID"] == bts_id, dict[option]] = ''
            else:
                user_choices[user_id][bts_id].update(option)

        # Respond to the button press
        await call.answer()



    except Exception as e:
        print(e)
        await call.answer(f"Noma'lum xatolik yuzaga keldi! <code>{e}</code>")

#user kirgizadigan kommentlarni yozish uchun
@dp.callback_query_handler(text_contains="comment")
async def add_comment(call: types.CallbackQuery, state:FSMContext):
    user_id = call.from_user.id
    user_name = call.from_user.first_name
    bts_id = call.data.split('_btsid')[1]

    # Ask the user for their comment
    await call.message.answer(f"{user_name} , {bts_id} obekti bo'yicha izohingizni kiriting:")

    # Set the state to capture the comment
    await FindId.comment.set()

    # Pass the bts_id as part of the state data
    await state.update_data(bts_id=bts_id)


# Add a message handler to capture the user's comment
@dp.message_handler(state=FindId.comment)
async def capture_comment(message: Message, state: FSMContext):
    # Get the comment from the message
    user_id = message.from_user.id
    user_name = message.from_user.first_name
    user_notation = message.from_user.username
    comment_text = message.text
    excel_data['Коментарий'] = excel_data["Коментарий"].astype(str)

    # Get the associated bts_id from the state data
    async with state.proxy() as data:
        bts_id = data.get("bts_id")
        excel_data.loc[excel_data["BTSID"] == bts_id, "Коментарий"] = comment_text + f" \n\nIzoh egasi <b>{user_name}</b>, " \
                                                                                     f"user_name:@{user_notation} user_id={user_id}" \
                                                                                     f" izoh saqlangan kun: {today_date}"

    # Do something with the comment and the associated bts_id
    # For example, you can store them together in a dictionary
    user_id = message.from_user.id
    if user_id in user_choices:
        if bts_id in user_choices[user_id]:
            user_choices[user_id][bts_id]["comment"] = comment_text
        else:
            user_choices[user_id][bts_id] = {"comment": comment_text}
    else:
        user_choices[user_id] = {bts_id: {"comment": comment_text}}

    # Inform the user that their comment has been recorded
    await message.answer(f"<code>{bts_id}</code> bo'yicha izohingiz saqlandi!")

    # Finish the state
    await state.finish()


@dp.callback_query_handler(text_contains="apply_changes")
async def show_user_choices(call: types.CallbackQuery):
    user_id = call.from_user.id
    user_name = call.from_user.first_name
    bts_id = call.data.split('_btsid')[1]
    option = call.data.split('_btsid')[0]
    selected = user_choices[user_id][bts_id]

    if selected:
        await call.message.answer(f"{user_name}, Siz {bts_id} uchun tanlaganlaringiz saqlandi!")
    else:
        await call.message.answer(f"{user_name}, Siz {bts_id} bo'yicha xech bir bo'limni tanlamadingiz!")

    await call.answer()

#_____________________________________________________________________________________________________________________#
#statistika bo'limi uchun handlerlar qismi
#bugungi reja uchun funksiya

@dp.message_handler(text='📆bugungi ishga tushish rejasi')
async def todays_launch_plan(message: Message):
    try:
        # Convert the "Запуск" column to datetime if it's not already in datetime format

        excel_data["Запуск в процессе"] = pd.to_datetime(excel_data["Запуск в процессе"], errors="coerce")


        # Filter the DataFrame for rows where the "Запуск" column equals today_date
        filtered_rows = excel_data[(excel_data["Запуск в процессе"].dt.strftime("%Y-%m-%d") == today_date_str)&
                                   (excel_data['Запуск'].isna() | (excel_data['Запуск'] == ''))]

        # Check if there are any rows matching today's date
        if not filtered_rows.empty:
            i = 0
            j = 0
            # If there are matching rows, send them as a message
            spiska_zapusk = ''
            spiska_modern = ''
            for index, row in filtered_rows.iterrows():
                bts_name = row["BTS Name"].title()
                bts_old_texnologiya = row["Существующая технология"]
                bts_texnologiya = row["Технология после модернизации"]
                if row["Online\\New sites"] in ["New Site","New site","new site", "NEW SITE"]:
                    bts_id_zapusk = row["BTSID"]
                    i += 1
                    spiska_zapusk = spiska_zapusk + f"<b>{i}. {bts_id_zapusk} {bts_name} </b>  {bts_texnologiya}\n\n"
                elif row["Online\\New sites"] in ["Online", "online", "ONLINE"]:
                    bts_id_modern = row["BTSID"]
                    j += 1
                    spiska_modern = spiska_modern + f"<b>{j}. {bts_id_modern}  {bts_name} </b> {bts_old_texnologiya} ⏩🆕  {bts_texnologiya} \n\n"

            await message.answer(f"<b>Bugun, {today_date_str} kuni yangi ishga tushirilishi rejalashtirilgan BS(lar) soni {i} ta:</b>\n"
                                 f"{spiska_zapusk}\n",                                 reply_markup=None)
            await message.answer(f"<b>Shuningdek, quyidagi {j} ta BS(lar)da SWAP va modernizatsiya ishlari rejalashtirilgan:</b>\n"
                                 f"{spiska_modern}\n",
                                 reply_markup=None)
        else:
            await message.answer(f"Bugun ishga tushirilishi rejalashtirilgan sayt topilmadi.")

    except Exception as e:
        print(e)
        await message.answer(f"Noma'lum xatolik yuzaga keldi! <code>{e}</code>")

#vaqt oralig'ida ishga tushganlarni chiqarish uchun funksiya

@dp.message_handler(text="📆vaqt oralig'ida ishga tushganlar")
async def launched_by(message: Message, state:FSMContext):

    # Ask the user for their time shift
    await message.answer("Qaysi vaqt oralig'ida ishga tushgan obektlarni ko'rmoqchisiz? \n"
                         "2024 chi yil 10 chi yanvardan , 2024 chi yil 31 chi martgacha bo'lgan oraliq uchun misol:  "
                         "<code>2024-01-01:2024-03-31</code> ko'rinishida.\n"
                         "kiritilgan ikki sanani '<code>:</code>' orqali ajrating. "
                         "Qidirayotgan oralliqni kirgazishingizda yuqoridagi namuna singari, hech qanday probelsiz kiritishingiz muxim!", reply_markup=None)

    # Set the state to capture the comment
    await FindId.time_shift.set()

# Add a message handler to capture the user's chosen time shift
@dp.message_handler(state=FindId.time_shift)
async def choosen_time_shift(message: Message, state: FSMContext):
    try:
        # Get the timeshift from the message
        user_id = message.from_user.id
        user_name = message.from_user.first_name
        user_notation = message.from_user.username
        time_shift = message.text

        begin_date, end_date = time_shift.split(":")
        begin_date = datetime.strptime(begin_date, '%Y-%m-%d')
        end_date = datetime.strptime(end_date, '%Y-%m-%d')


        #excel_data['Запуск'] = excel_data["Запуск"].dt.strftime("%Y-%m-%d")
        await message.answer(f"{begin_date} dan {end_date} gacha vaqt oralig'ida ishga tushgan va"
                             f" modernizatsiya bo'lgan BS(lar) ro'yxati\n")

        # Convert the "Запуск" column to datetime format
        excel_data['Запуск'] = pd.to_datetime(excel_data['Запуск'], errors="coerce")

        # Filter data between two dates using dt.strftime()
        filtered_df = excel_data[(excel_data['Запуск'] >= begin_date) & (excel_data['Запуск'] <= end_date)]

        if not filtered_df.empty:
            # Initialize the string variable outside the loop
            bs_new = ''
            bs_moder = ''
            new = 0
            moder = 0
            filtered_df['Запуск'] = filtered_df['Запуск'].dt.strftime("%Y-%m-%d")
            # Iterate through each row and select 'BTSID', 'BTS Name', and 'Запуск' columns
            for ind, row in filtered_df.iterrows():
                #yangi ishga tushgan va modernizatsiya bo'lganlarni alohida alohida chiqazadi
                if row["Online\\New sites"] in ["New Site","New site","new site", "NEW SITE"]:
                    new += 1
                    bs_new += f"\n{new}. <b>{row['BTSID']}</b>  {row['BTS Name'].title()}  {row['Запуск']}"
                elif row["Online\\New sites"] in ["Online", "online", "ONLINE"]:
                    moder += 1
                    bs_moder += f"\n{moder}. <b>{row['BTSID']}</b>  {row['BTS Name'].title()}  {row['Запуск']}"

            if new > 0:
                await message.answer(f"{begin_date} dan {end_date} oralig'ida {new} ta yangi obekt ishga tushgan"
                                     f"\nBS(lar) ro'yxati \n{bs_new}\n", reply_markup=None)
            else:
                pass
            if moder > 0:
                await message.answer(f"va {begin_date} dan {end_date} vaqt oralig'ida {moder} ta obekt yangi texnologiyaga "
                                     f"modernizatsiya bo'lgan \nBS(lar) ro'yxati \n{bs_moder}\n", reply_markup=None)
            else:
                pass
        else:
            await message.answer(f"{begin_date} dan {end_date} oralig'ida ishga tushgan BS(lar) bo'yicha ma'lumot topilmadi!")

    except Exception as e:
        print(e)
        await message.answer(f"Noma'lum xatolik yuzaga keldi! <code>{e}</code>")


    # Finish the state
    await state.finish()


#⚙️bugungi bajarilgan ishlar uchun qism

@dp.message_handler(text='⚙️bugungi bajarilgan ishlar')
async def todays_done(message: Message):
    try:

        # Convert the "Доставка на объект", "Монтаж в процессе", "Монтаж заверщен" columns
        # to datetime if it's not already in datetime format
        excel_data["Запуск"] = pd.to_datetime(excel_data["Запуск"], errors="coerce").dt.date
        excel_data["Доставка на объект"] = pd.to_datetime(excel_data["Доставка на объект"], errors="coerce").dt.date
        excel_data["Монтаж в процессе"] = pd.to_datetime(excel_data["Монтаж в процессе"], errors="coerce").dt.date
        excel_data["Монтаж заверщен"] = pd.to_datetime(excel_data["Монтаж заверщен"], errors="coerce").dt.date
        excel_data["BTS Name"] = excel_data["BTS Name"].astype(str)

        # Check if there are any rows matching today's date
        if not excel_data.empty:
            # If there are matching rows, send them as a message
            y = 0
            i = 0
            j = 0
            x = 0
            zapusk_today= ''
            dostavka_vobekt = ''
            montaj_nachat = ''
            montaj_zavershyon = ''

            for index, row in excel_data.iterrows():
                bts_id = row["BTSID"]
                bts_name = row["BTS Name"].title()
                bts_old_texnologiya = row["Существующая технология"]
                bts_texnologiya = row["Технология после модернизации"]
                if row["Запуск"] == bugun:
                    y += 1
                    zapusk_today += f"<b>{y}. {bts_id}  {bts_name} </b> {bts_old_texnologiya} ⏩🆕  {bts_texnologiya}\n"
                elif row["Монтаж заверщен"] == bugun:
                    x += 1
                    montaj_zavershyon += f"<b>{x}. {bts_id}  {bts_name} </b> {bts_old_texnologiya} ⏩🆕  {bts_texnologiya}\n"
                elif row["Монтаж в процессе"] == bugun:
                    j += 1
                    montaj_nachat += f"<b>{j}. {bts_id}  {bts_name} </b> {bts_old_texnologiya} ⏩🆕  {bts_texnologiya}\n"
                if row["Доставка на объект"] == bugun:
                    i += 1
                    dostavka_vobekt += f"<b>{i}. {bts_id}  {bts_name} </b>  {bts_old_texnologiya} ⏩🆕  {bts_texnologiya}\n"
                else:
                    pass

            if y > 0:
                await message.answer(f"<b>Bugun, {bugun} quyidagi {y} ta obekt ishga tushdi:</b>\n"
                                     f"{zapusk_today}\n", reply_markup=None)
            else:
                pass
            if x > 0:
                await message.answer(f"<b>Bugun, {bugun} quyidagi {x} ta obektta montaj ishlari tugallandi:</b>\n"
                                     f"{montaj_zavershyon}\n", reply_markup=None)
            else:
                pass
            if j > 0:
                await message.answer(f"<b>Quyidagi {j} ta obektta montaj ishlari boshlandi:</b>\n"
                                     f"{montaj_nachat}\n", reply_markup=None)
            else:
                pass
            if i > 0:
                await message.answer(f"<b>Shuningdek, quyidagi {i} ta obektga qurilmalar yetkazildi:</b>\n"
                                     f"{dostavka_vobekt}\n", reply_markup=None)
            else:
                pass
        else:
            await message.answer(f"Bugun biror saytda ish qilingani xaqida ma'lumot topilmadi.")

    except Exception as e:
        print(e)
        await message.answer(f"Noma'lum xatolik yuzaga keldi! <code>{e}</code>")

#_____________________________________________________________________________________________________________________#

#⚙️jarayonda uchun qism

@dp.message_handler(text='⚙️jarayonda')
async def in_progress(message: Message):
    try:
        # Convert the "Доставка на объект", "Монтаж в процессе", "Монтаж заверщен" columns
        # to datetime if it's not already in datetime format
        excel_data["Доставка на объект"] = pd.to_datetime(excel_data["Доставка на объект"], errors="coerce").dt.date
        excel_data["Монтаж в процессе"] = pd.to_datetime(excel_data["Монтаж в процессе"], errors="coerce").dt.date
        excel_data["Монтаж заверщен"] = pd.to_datetime(excel_data["Монтаж заверщен"], errors="coerce").dt.date
        excel_data["BTS Name"] = excel_data["BTS Name"].astype(str)


        # Check if there are any rows matching today's date
        if not excel_data.empty:
            # If there are matching rows, send them as a message
            i = 0
            j = 0
            x = 0
            dostavka_vobekt = ''
            montaj_nachat = ''
            ne_zapushen = ''

            for index, row in excel_data.iterrows():
                bts_id = row["BTSID"]
                bts_name = row["BTS Name"].title()
                koment1 = row["Примечание"]
                koment2 = row["Коментарий"]
                # Check if the row["Монтаж заверщен"] value is not NaT and row["Запуск"] value is not Na
                if pd.notna(row["Монтаж заверщен"]) and pd.isna(row["Запуск"]):
                    # Define Монтаж заверщен date
                    sites_date = row["Монтаж заверщен"]

                    # Calculate the difference in days
                    day_difference = (bugun - sites_date).days
                    x += 1
                    ne_zapushen += f"<b>{x}. {bts_id} </b> {bts_name}  {day_difference} kundan beri.\n"

            await message.answer(f"<b>quyidagi {x} ta obektlarda montaj ishlari yakunlangan, lekin ishga tushmagan:</b>\n"
                                 f"{ne_zapushen}\n",
                                 reply_markup=None)
        else:
            await message.answer(f"Jarayonda turgan obektlar mavjud emas!")

    except Exception as e:
        print(e)
        await message.answer(f"Noma'lum xatolik yuzaga keldi! <code>{e}</code>")

#_____________________________________________________________________________________________________________________#
#faylni serverdan yuklab olish uchun xali tugallanmadi
async def download_excel_file():
    # Specify the path to save the Excel file
    excel_file_path = "my_excel_file.xlsx"

    # Save the DataFrame to an Excel file
    excel_data["BTS Name"].str.title()
    excel_data.to_excel(excel_file_path, sheet_name="ZTE_&_HUAWEI", index=False)

    # Read the saved Excel file as bytes
    with open(excel_file_path, "rb") as file:
        file_content = io.BytesIO(file.read())

    # Return the file content and filename
    return file_content, "my_excel_file.xlsx"


# Modify the message handler to download the file and send it back to the user
@dp.message_handler(text="⬇️ serverdan faylni yuklab olish")
async def faylni_serverdan_yukla(message: Message):
    if is_admin(message.from_user.id):
        await message.answer("📎📊📈 Faylni serverdan qabul qilib oling\n yuklanmoqda...", reply_markup=ReplyKeyboardRemove())
        try:
            # Download the Excel file
            file_content, original_filename = await download_excel_file()

            # Send the Excel file to the user
            await message.answer_document(document=file_content, caption=original_filename)
        except Exception as e:
            await message.reply(f"❌❓Xatolik yuzaga keldi: <b>{str(e)}</b>\n"
                                f"Iltimos qaytadan urinib ko'ring!")
    else:
        await message.answer("🚫Siz admin emassiz, fayl yuklolmaysiz!", reply_markup=ReplyKeyboardRemove())
#_____________________________________________________________________________________________________________________#