import telebot
import admin
import logging
import datetime
import keyboard
import pymysql
from wrapperDB import insert_record
from wrapperDB import select_pb

bot = telebot.TeleBot(admin.token)

logging.basicConfig(filename='log_err.log', level=logging.ERROR,
                    format='\n#######################################################################################\n'
                           '%(asctime)s - %(levelname)s - %(message)s')
my_log_filename = "log.txt"

db = pymysql.connect(user=admin.connectDB_user, passwd=admin.connectDB_passwd,
                     host=admin.connectDB_host, port=admin.connectDB_port, db=admin.connectDB_name)
db.set_charset('utf8')

keyboard_main = keyboard.get_keyboard_main()


def my_logger(message, answer, logfile):
    logfile.write("\n----------------\n")

    if message.from_user.last_name is not None:

        logfile.write("Сообщение от {0} {1}. (id = {2})\n Текст = {3}\n".format(message.from_user.first_name,
                                                                                message.from_user.last_name,
                                                                                str(message.from_user.id),
                                                                                message.text))
    else:

        logfile.write("Сообщение от {0}. (id = {1})\n Текст = {2}\n".format(message.from_user.first_name,
                                                                            str(message.from_user.id),
                                                                            message.text))

    logfile.write(str(datetime.datetime.now().replace(microsecond=0)) + "\n")
    logfile.write("Answer = " + answer + "\n")


@bot.message_handler(commands=['start'])
def print_start(message):
    bot.send_message(message.chat.id, "Let's go!", reply_markup=keyboard_main)


@bot.message_handler(commands=['get_publications'])
def print_settings(message):
    if message.chat.id == admin.admin_id:
        bot.send_message(message.chat.id, "Ваш запрос в обработке", reply_markup=keyboard_main)
        select_pb(db, bot, message.chat.id)
    else:
        bot.send_message(message.chat.id, admin.perm_den + "\nЗапросите права доступа у администрации",
                         reply_markup=keyboard_main)


@bot.message_handler(commands=['get_publications_by_year'])
def print_settings(message):
    if message.chat.id == admin.admin_id:
        bot.send_message(message.chat.id, "Ваш запрос в обработке", reply_markup=keyboard_main)
        select_pb(db, bot, message.chat.id)
    else:
        bot.send_message(message.chat.id, admin.perm_den + "\nЗапросите права доступа у администрации",
                         reply_markup=keyboard_main)


@bot.message_handler(content_types=['text'])
def dialog(message):
    bot.send_message(message.chat.id, "Echo:\n" + message.text, reply_markup=keyboard_main)

    logfile = open(my_log_filename, "a")
    my_logger(message, message.text, logfile)
    logfile.close()


if __name__ == '__main__':

    try:

        bot.polling(none_stop=True, interval=0)

    except:

        logging.exception('')
        raise
