import telebot

takel = lambda r: r.readline().strip('\n')

with open('secret.txt') as secret:
    project_name = takel(secret)
    bot = telebot.TeleBot(takel(secret))
    proxy_address = takel(secret)
    if proxy_address:
        telebot.apihelper.proxy = {'https': proxy_address}

import user
user.load_db(project_name)

#import task

tasklist = list()

@bot.message_handler(commands=['start'])
def identify_message(msg):
    u = msg.from_user
    if user.check(u):
        bot.send_message(msg.chat.id, 'Привет, {0}!'.format(user.name(u)))
        user.update(u)
    else:
        bot.send_message(msg.chat.id, 'Привет! Не узнаю тебя :( Напомни плиз секретное слово)')
        bot.register_next_step_handler(msg, check_password)

def check_password(msg):
    if msg.text.lower() == 'кусь':
        bot.send_message(msg.chat.id, 'Добро пожаловать {0}!'.format(
            user.name(msg.from_user)))
        user.register(msg.from_user)
        remind_instructions(msg)
    else:
        bot.send_message(msg.chat.id, 'Увы, не в этот раз.')

@bot.message_handler(commands=['help'])
def remind_instructions(msg):
    bot.send_message(msg.chat.id, 'Используй комманду /add чтобы добавить задачу, /status чтобы изменить статус выполнения задачи, /edit чтобы изменить саму задачу, /show чтобы вывести задачи в которых ты упомянут, /show_all чтобы вывести все задачи.')

bot.polling()
