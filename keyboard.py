from telebot import types

button_get_publications = types.InlineKeyboardButton(text="/get_publications")
button_get_publications_by_year = types.InlineKeyboardButton(text="/get_publications_by_year")


def get_keyboard_main():
    keyboard_main = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)

    keyboard_main.add(button_get_publications, button_get_publications_by_year)

    return keyboard_main
