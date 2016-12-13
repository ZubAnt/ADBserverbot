import telebot
import admin
import logging
import datetime
import keyboard
import pymysql
from wrapperDB import select_pb
from wrapperDB import select_pb_by_year
from wrapperDB import select_year_by_pb

bot = telebot.TeleBot(admin.token)

logging.basicConfig(filename='log_err.log', level=logging.ERROR,
                    format='\n#######################################################################################\n'
                           '%(asctime)s - %(levelname)s - %(message)s')
my_log_filename = "log.txt"

db = pymysql.connect(user=admin.connectDB_user, passwd=admin.connectDB_passwd,
                     host=admin.connectDB_host, port=admin.connectDB_port, db=admin.connectDB_name)
db.set_charset('utf8')

keyboard_main = keyboard.get_keyboard_main()
keyboard_year = keyboard.get_keyboard_year()

flag_insert_year = dict()          # Key = id, Value = True or False


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


def my_send_message_by_year(id_in, data_list_in):
    if not data_list_in:
        bot.send_message(id_in, "Пусто", reply_markup=keyboard_main)
    else:
        cnt = 1
        answer = ""
        size = len(data_list_in)
        for data in data_list_in:
            answer += str(cnt) + '. ' + data + "\n"
            if cnt % 10 == 0 or cnt == size:
                if cnt == size:
                    bot.send_message(id_in, answer, reply_markup=keyboard_main)
                else:
                    bot.send_message(id_in, answer + '\nОсталось ' + str(size - cnt) + 'записей',
                                     reply_markup=keyboard_main)
                answer = ""
            cnt += 1


def my_send_message_all(id_in, data_list_in):
    if not data_list_in:
        bot.send_message(id_in, "Пусто", reply_markup=keyboard_main)
    else:
        cnt = 1
        answer = ""
        size = len(data_list_in)
        for data in data_list_in:
            year = select_year_by_pb(db, data)
            if year is None:
                year = "unknown"
            answer += str(cnt) + '. ' + data + ". Год издания - " + str(year) + "\n"
            if cnt % 10 == 0 or cnt == size:
                if cnt == size:
                    bot.send_message(id_in, answer, reply_markup=keyboard_main)
                else:
                    bot.send_message(id_in, answer + '\nОсталось ' + str(size - cnt) + 'записей',
                                     reply_markup=keyboard_main)
                answer = ""
            cnt += 1


@bot.message_handler(commands=['start'])
def print_start(message):
    bot.send_message(message.chat.id, "Let's go!", reply_markup=keyboard_main)


@bot.message_handler(commands=['get_publications'])
def print_settings(message):
    if message.chat.id == admin.admin_id:

        bot.send_message(message.chat.id, "Ваш запрос в обработке", reply_markup=keyboard_main)
        data_list = select_pb(db)
        my_send_message_all(message.chat.id, data_list)
    else:
        bot.send_message(message.chat.id, admin.perm_den + "\nЗапросите права доступа у администрации",
                         reply_markup=keyboard_main)


@bot.message_handler(commands=['get_publications_by_year'])
def print_settings(message):
    if message.chat.id == admin.admin_id:
        flag_insert_year[message.chat.id] = True
        bot.send_message(message.chat.id, "Введите год издания", reply_markup=keyboard_year)
    else:
        bot.send_message(message.chat.id, admin.perm_den + "\nЗапросите права доступа у администрации",
                         reply_markup=keyboard_main)


@bot.message_handler(content_types=['text'])
def dialog(message):

    if flag_insert_year.get(message.chat.id) is True:
        try:
            year = int(message.text)
            bot.send_message(message.chat.id, "Производится поиск статей за " + message.text + " год:",
                             reply_markup=keyboard_main)
            data_list = select_pb_by_year(db, year)
            my_send_message_by_year(message.chat.id, data_list)

        except ValueError:   # Handle the exception

            bot.send_message(message.chat.id, "ERROR: BAD INTEGER", reply_markup=keyboard_main)

        flag_insert_year[message.chat.id] = False

    else:
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
