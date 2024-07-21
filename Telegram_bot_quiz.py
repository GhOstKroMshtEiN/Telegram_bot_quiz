import telebot
from telebot import types
import random

TOKEN_TELEGRAM = 'XXX'
bot = telebot.TeleBot(TOKEN_TELEGRAM)
Total_PROGRESS_of_RESPONCES = {}


@bot.message_handler(commands=['start'])
def start_message(message):
    chat_id = message.chat.id
    Total_PROGRESS_of_RESPONCES[chat_id] = 0
    bot.send_message(message.chat.id, 'Добро пожаловать в игру угадай число')
    markup = types.ReplyKeyboardMarkup()
    btn_1 = types.KeyboardButton('Да')
    btn_2 = types.KeyboardButton('Нет')
    btn_3 = types.KeyboardButton('Посмотреть исходный код на сайте GitHub')
    markup.add(btn_1, btn_2, btn_3)
    bot.send_message(message.chat.id, 'Вы хотите продолжить', reply_markup=markup)


@bot.message_handler(func=lambda message: message.text.lower() == 'да')
def yes_choice(message):
    bot.send_message(message.chat.id, 'Введите максимальное число рандома')
    bot.register_next_step_handler(message, func_log)


def func_log(message):
    try:
        text_message = message.text
        result = random.randint(0, int(text_message))
        bot.send_message(message.chat.id, f'Число загаданно.')
        bot.send_message(message.chat.id, 'Попробуй угадать число:')
        bot.register_next_step_handler(message, call, result)
    except ValueError:
        bot.send_message(message.chat.id, 'Неверный формат ввода. Пожалуйста повторите попытку')
        bot.register_next_step_handler(message, func_log)


def call(message, result):
    try:
        text_random = int(message.text)
        result = message.chat.id
        if text_random > 0:
            if text_random == result:
                bot.send_message(message.chat.id, f'Вы угадали число. Ваше загаданное число --> {result}')
            elif text_random > result:
                bot.send_message(message.chat.id, 'Загаданное число меньше <-- :)')
                bot.register_next_step_handler(message, call, result)
            else:
                bot.send_message(message.chat.id, 'Загаданное число больше --> :)')
                bot.register_next_step_handler(message, call, result)
        else:
            bot.send_message(message.chat.id, 'Число не должно быть меньше нуля. Пожалуйста повторите попытку')
            bot.register_next_step_handler(message, call, result)
    except ValueError:
        bot.send_message(message.chat.id, 'Неверный формат ввода. Пожалуйста введите целое число')
        bot.register_next_step_handler(message, call, result)


@bot.message_handler(func=lambda message: message.text.lower() == 'нет')
def message_quiz(message):
    bot.send_message(message.chat.id, 'Плохой выбор')
    bot.send_message(message.chat.id, 'Играем в викторину')
    message_func_quiz(message)


def message_func_quiz(message):
    markup = types.InlineKeyboardMarkup(row_width=2)
    btn_1 = types.InlineKeyboardButton('Солнце', callback_data='quiz1_Солнце')
    btn_2 = types.InlineKeyboardButton('Меркурий', callback_data='quiz1_Меркурий')
    btn_3 = types.InlineKeyboardButton('Марс', callback_data='quiz1_Марс')
    btn_4 = types.InlineKeyboardButton('Земля', callback_data='quiz1_Земля')
    markup.add(btn_1, btn_2, btn_3, btn_4)
    bot.send_message(message.chat.id, "Какая планета самая ближняя к Солнцу?", reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data.startswith('quiz1_'))
def handle_quiz_answer(call):
    chat_id = call.message.chat.id
    answer = call.data.split('_')[1]
    if answer == 'Меркурий':
        bot.send_message(chat_id,
                         'Правильно! --> Меркурий — это самая близкая к Солнцу планета нашей Солнечной системы. Он расположен на среднем расстоянии около 58 миллионов километров (36 миллионов миль) от Солнца. Из-за своей близости к Солнцу, Меркурий имеет очень высокие дневные температуры и очень низкие ночные температуры. Планета совершает полный оборот вокруг Солнца примерно за 88 земных дней.')

        Total_PROGRESS_of_RESPONCES[chat_id] += 1
        ask_next_question(call.message)
    else:
        bot.send_message(chat_id, 'Неправильно, правильный ответ: Меркурий')
        ask_next_question(call.message)


def ask_next_question(message):
    markup = types.InlineKeyboardMarkup(row_width=2)
    btn_1 = types.InlineKeyboardButton('Гипотенуза', callback_data='quiz2_Гипотенуза')
    btn_2 = types.InlineKeyboardButton('Катет', callback_data='quiz2_Катет')
    btn_3 = types.InlineKeyboardButton('Диагональ', callback_data='quiz2_Диагональ')
    btn_4 = types.InlineKeyboardButton('Периметр', callback_data='quiz2_Периметр')
    markup.add(btn_1, btn_2, btn_3, btn_4)
    bot.send_message(message.chat.id, "Как называется самая длинная сторона прямоугольного треугольника?",
                     reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data.startswith('quiz2_'))
def handle_next_question(call):
    chat_id = call.message.chat.id
    answer = call.data.split('_')[1]
    if answer == 'Гипотенуза':
        bot.send_message(chat_id,
                         'Правильно! Гипотенуза - это самая длинная сторона прямоугольного треугольника.')
        Total_PROGRESS_of_RESPONCES[chat_id] += 1
    else:
        correct_answer = 'Гипотенуза'
        bot.send_message(chat_id, f'Неправильно, правильный ответ: {correct_answer}')
    ask_next_question_3(call.message)


def ask_next_question_3(message):
    markup = types.InlineKeyboardMarkup(row_width=2)
    btn_1 = types.InlineKeyboardButton('Литр', callback_data='quiz3_Литр')
    btn_2 = types.InlineKeyboardButton('Килограмм', callback_data='quiz3_Килограмм')
    btn_3 = types.InlineKeyboardButton('Моль', callback_data='quiz3_Моль')
    btn_4 = types.InlineKeyboardButton('Джоуль', callback_data='quiz3_Джоуль')
    markup.add(btn_1, btn_2, btn_3, btn_4)
    bot.send_message(message.chat.id, "Как называется величина, характеризующая количество вещества?",
                     reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data.startswith('quiz3_'))
def handler_next_question3(call):
    chat_id = call.message.chat.id
    answer = call.data.split('_')[1]
    if answer == 'Моль':
        bot.send_message(chat_id,
                         'Молодец! Это правильный ответ.\nПояснение: --> Моль — это единица измерения количества вещества в Международной системе единиц (СИ). Один моль содержит ровно столько атомов, молекул или других частиц, сколько содержится в 12 граммах углерода-12, что составляет примерно 6.022 x 10^23 частиц (число Авогадро).')
        Total_PROGRESS_of_RESPONCES[chat_id] += 1
    else:
        correct_answer = 'Моль'
        bot.send_message(chat_id, f'Ответ неверный. Правильный ответ: {correct_answer}')
    ask_next_question_4(call.message)


def ask_next_question_4(message):
    markup = types.InlineKeyboardMarkup(row_width=2)
    btn_1 = types.InlineKeyboardButton('Секущая', callback_data='quiz4_Секущая')
    btn_2 = types.InlineKeyboardButton('Диаметр', callback_data='quiz4_Диаметр')
    btn_3 = types.InlineKeyboardButton('Хорда', callback_data='quiz4_Хорда')
    btn_4 = types.InlineKeyboardButton('Радиус', callback_data='quiz4_Радиус')
    markup.add(btn_1, btn_2, btn_3, btn_4)
    bot.send_message(message.chat.id,
                     "Как называется отрезок, соединяющий центр окружности с любой точкой на окружности?",
                     reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data.startswith('quiz4_'))
def handler_next_question4(call):
    chat_id = call.message.chat.id
    answer = call.data.split('_')[1]
    if answer == 'Радиус':
        bot.send_message(chat_id,
                         'Правильно! Радиус — это отрезок, соединяющий центр окружности с любой точкой на окружности.')
        Total_PROGRESS_of_RESPONCES[chat_id] += 1
    else:
        correct_answer = 'Радиус'
        bot.send_message(chat_id, f'Ответ неверный. Правильный ответ: {correct_answer}')
    ask_next_question_5(call.message)


def ask_next_question_5(message):
    markup = types.InlineKeyboardMarkup(row_width=2)
    btn_1 = types.InlineKeyboardButton('Квадратичная', callback_data='quiz5_Квадратичная')
    btn_2 = types.InlineKeyboardButton('Линейная', callback_data='quiz5_Линейная')
    btn_3 = types.InlineKeyboardButton('Кубическая', callback_data='quiz5_Кубическая')
    btn_4 = types.InlineKeyboardButton('Логарифмическая', callback_data='quiz5_Логарифмическая')
    markup.add(btn_1, btn_2, btn_3, btn_4)
    bot.send_message(message.chat.id,
                     "Как называется математическая функция, представляющая пропорциональную зависимость y = kx?",
                     reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data.startswith('quiz5_'))
def handler_next_question5(call):
    chat_id = call.message.chat.id
    answer = call.data.split('_')[1]
    if answer == 'Линейная':
        bot.send_message(chat_id,
                         'Правильно! Линейная функция представляет собой прямую линию на графике и описывает пропорциональную зависимость между переменными.')
        Total_PROGRESS_of_RESPONCES[chat_id] += 1
    else:
        correct_answer = 'Линейная'
        bot.send_message(chat_id, f'Ответ неверный. Правильный ответ: {correct_answer}')
    ask_next_question_6(call.message)


def ask_next_question_6(message):
    markup = types.InlineKeyboardMarkup(row_width=2)
    btn_1 = types.InlineKeyboardButton('Атом', callback_data='quiz6_Атом')
    btn_2 = types.InlineKeyboardButton('Молекула', callback_data='quiz6_Молекула')
    btn_3 = types.InlineKeyboardButton('Ион', callback_data='quiz6_Ион')
    btn_4 = types.InlineKeyboardButton('Протон', callback_data='quiz6_Протон')
    markup.add(btn_1, btn_2, btn_3, btn_4)
    bot.send_message(message.chat.id,
                     "Как называется самая малая частица химического элемента, сохраняющая его свойства?",
                     reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data.startswith('quiz6_'))
def handler_next_question6(call):
    chat_id = call.message.chat.id
    answer = call.data.split('_')[1]
    if answer == 'Атом':
        bot.send_message(chat_id,
                         'Правильно! Атом — это наименьшая частица химического элемента, которая сохраняет его химические свойства.')
        Total_PROGRESS_of_RESPONCES[chat_id] += 1
    else:
        correct_answer = 'Атом'
        bot.send_message(chat_id, f'Ответ неверный. Правильный ответ: {correct_answer}')
    Value_results(call.message)


def Value_results(message):
    chat_id = message.chat.id
    score = Total_PROGRESS_of_RESPONCES[chat_id]
    bot.send_message(chat_id, f'Ваш результат: {score}/6')

