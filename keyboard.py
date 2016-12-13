from telebot import types

button_get_publications = types.InlineKeyboardButton(text="/get_publications")
button_get_publications_by_year = types.InlineKeyboardButton(text="/get_publications_by_year")


button_1 = types.InlineKeyboardButton(text="2008")
button_2 = types.InlineKeyboardButton(text="2009")
button_3 = types.InlineKeyboardButton(text="2010")
button_4 = types.InlineKeyboardButton(text="2011")
button_5 = types.InlineKeyboardButton(text="2012")
button_6 = types.InlineKeyboardButton(text="2013")
button_7 = types.InlineKeyboardButton(text="2014")
button_8 = types.InlineKeyboardButton(text="2015")
button_9 = types.InlineKeyboardButton(text="2016")


def get_keyboard_main():
    keyboard_main = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)

    keyboard_main.add(button_get_publications, button_get_publications_by_year)

    return keyboard_main


def get_keyboard_year():

    keyboard_year = types.ReplyKeyboardMarkup(row_width=3, resize_keyboard=True)

    keyboard_year.add(button_1, button_2, button_3,
                      button_4, button_5, button_6,
                      button_7, button_8, button_9)

    return keyboard_year
