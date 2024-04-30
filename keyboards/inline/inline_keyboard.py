from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

class InlineKeyboardBuilder:
    def __init__(self):
        self.keyboard = []

    def add_button(self, text, callback_data):
        button = InlineKeyboardButton(text=text, callback_data=callback_data)
        self.keyboard.append([button])

    def create_keyboard(self):
        return InlineKeyboardMarkup(inline_keyboard=self.keyboard)





choices = ["supply_eq","fit_eq","finish_fit_eq","launch_ongoing","launch_finish"]


#another way of making inline buttons
# # Create an instance of InlineKeyboardMarkup
# optionalSelect = InlineKeyboardMarkup()
#
#
# # Define your options
# options = ["🚚qurilma yetkazish", "🅿️🛠montaj jarayonida", "✅🛠montaj tugallandi", "🅿️⚙️ishga tushirish jarayonida",
#            "✅📶ishga tushdi","📋izoh"]
#
# # Add buttons for each option to the keyboard
# for option in options:
#     button = InlineKeyboardButton(text=option, callback_data=f"select_option_{options.index(option) + 1}")
#     optionalSelect.add(button)

