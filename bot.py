import telebot

import config
import markup

bot = telebot.TeleBot(config.token)
telebot.apihelper.proxy = {'https': config.proxy}

import user
import task

@bot.message_handler(commands=['start'])
@user.wrap
def identify_message(u, m):
    if u.authorized:
        bot.send_message(m.chat.id, 'Привет, {0}!'.format(u.name))
    else:
        bot.send_message(m.chat.id, 'Привет! Не узнаю тебя :( Напомни секретное слово')
        bot.register_next_step_handler(m, check_password)

@user.wrap
def check_password(u, m):
    if m.text.lower() == config.secret:
        bot.send_message(m.chat.id, 'Добро пожаловать {0}!'.format(u.name))
        u.register()
        remind_instructions(m)
    else:
        bot.send_message(m.chat.id, 'Неверное секретное слово.')

@bot.message_handler(func=lambda m: not user.User(m.from_user).authorized)
def not_authorized_message(m):
    bot.send_message(m.chat.id, 'Вы не авторизованы')

@bot.message_handler(commands=['help'])
def remind_instructions(m):
    bot.send_message(m.chat.id, '''Список комманд:
/new : добавить задачу
/append : добавить комментарии к уже созданной задаче
/status :  изменить статус выполнения задачи
/show : вывести задачи в которых ты упомянут
/show_all : вывести все задачи {0}'''.format(config.name))

@bot.message_handler(commands=['new'])
@user.wrap
def new_task_header(u, m):
    u.state.new_task(task.Task())
    bot.send_message(msg.chat.id, 'Введи заголовок задачи')
    bot.register_next_step_handler(msg, new_task_description)

def new_task_description(msg):
    t = task.new(msg.text, msg.from_user)
    bot.send_message(msg.chat.id, 'Добавь описание')
    bot.register_next_step_handler(msg, lambda m: new_task_priority_deadline(m, t))

def new_task_priority_deadline(msg):
    t.descripiton = msg.text
    bot.send_message(msg.chat.id, 'Опиши приоритет и сроки выполнения задачи. Можно указать "срочно", "важно", "желательно", "не важно", а также любую дату и время, например "четверг 17:30" или "20.11.2019"')
    #bot.register_next_step_handler(msg, 

def new_task_participants(msg, t):
    for p in t.potentional_participants:
        bot.send_message('Новая задача для тебя, {0}!'.format(p.author),
                         chat_id=p.author.id)
        bot.send_message(t.to_message())
        bot.send_message()

@bot.message_handler(commands=['show'])
def show_user_tasks(msg):
    any_tasks = False
    for t in task.show_user(msg.from_user):
        any_tasks = True
        bot.send_message(msg.chat.id, t.to_message())
    if not any_tasks:
        bot.send_message(msg.chat.id, 'У тебя нет заданий :(')

@bot.message_handler(commands=['show_all'])
def show_all_tasks(msg):
    for t in task.show_all():
        bot.send_message(msg.chat.id, t.to_message())

@bot.message_handler(commands=['status'])
def change_status(msg):
    bot.send_message(msg.chat.id, 'Введи номер задачи или часть заголовка')

@bot.message_handler(commands=['subscribe_tag'])
def subscribe(msg):
    bot.send_message(msg.chat.id, 'Напиши хештег на который ты хочешь подписаться')

@bot.message_handler(commands=['unsubscribe_tag'])
def unsubscribe(msg):
    bot.send_message
    

bot.polling()
