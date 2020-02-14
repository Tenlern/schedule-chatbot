import telebot
from database import DB

# Global Constants


# Global variables
database = DB("bot.db")
bot = telebot.TeleBot(Api_Token)

commands = {
    'start': 'Say welcome to bot',
    'help': 'Get info about commands',
    'today': 'Show schedule for today',
    'week': 'Show schedule for this week',

}


# Commands
@bot.message_handler(commands=['start'])
def send_welcome(message):
    if database.addUser(message.chat.id, message.chat.username):
        bot.send_message(message.chat.id, "Добро пожаловать!")
    else:
        bot.send_message(message.chat.id, "С возвращением!")


@bot.message_handler(commands=['help'])
def send_help(message):
    help_text = "The following commands are available: \n"
    for key in commands:
        help_text += "/" + key + ": " + commands[key] + "\n"
    bot.send_message(message.chat.id, help_text)  # send the generated help page


@bot.message_handler(commands=['today'])
def send_today(message):
    bot.send_message(message.chat.id, "Расписание на сегодня ():\n")  # send the generated help page


# Photo & documents
@bot.message_handler(content_types=['document', 'photo'])
def answer_photo_doc(message):
    print('*')
    bot.send_message(message.chat.id, "Мне кажется, что здесь написано, что ты хороший человек")


# Text messages which match regular expression
# Message about today
@bot.message_handler(regexp="\d*сегодня\d*")
def answer_today(message):
    print('*')
    bot.send_message(message.chat.id, "Расписание на сегодня ():\n")


# Message about tomorrow
@bot.message_handler(regexp="\d*завтра\d*")
def answer_tomorrow(message):
    print('*')
    bot.send_message(message.chat.id, "Расписание на завтра ():\n")


# Message about week
@bot.message_handler(regexp="\d*недел\d*")
def answer_week(message):
    print('*')
    bot.send_message(message.chat.id, "Расписание на неделю ():\n")


# Text messages
@bot.message_handler(content_types= ['text'])
def answer_text(message):
    pass


if __name__ == '__main__':
    bot.polling(interval=3)
