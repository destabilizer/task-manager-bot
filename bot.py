import telebot

takel = lambda r: r.readline().strip('\n')

with open('secret.txt') as secret:
    bot = telebot.TeleBot(takel(secret))
    proxy_address = takel(secret)
    if proxy_address:
        telebot.apihelper.proxy = {'https': proxy_address}

logged_users = list()
tasklist = list()

username = lambda u: u.first_name

@bot.message_handler(commands=['start'])
def identify_message(msg):
    user = msg.from_user
    if user in logged_users:
        bot.send_message(msg.chat.id, 'Привет, {0}!'.format(username(user)))
    else:
        bot.send_message(msg.chat.id, 'Привет! Не узнаю тебя :( Напомни плиз секретное слово)')
        bot.register_next_step_handler(msg, check_password)

def check_password(msg):
    if msg.text.lower() == 'кусь':
        bot.send_message(msg.chat.id, 'Добро пожаловать {0}!'.format(
            username(msg.from_user)))
        remind_instructions(msg)
    else:
        bot.send_message(msg.chat.id, 'Увы, не в этот раз.')

@bot.message_handler(commands=['help'])
def remind_instructions(msg):
    bot.send_message(msg.chat.id, 'Используй комманду /add чтобы добавить задачу, /status чтобы изменить статус выполнения задачи, /edit чтобы изменить саму задачу, /show чтобы вывести задачи в которых ты участвуешь.')

bot.polling()
