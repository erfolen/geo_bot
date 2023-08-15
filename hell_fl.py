from flask import Flask, request
from dotenv import load_dotenv
import os
import json
import requests
from os.path import join, dirname
import data_bot_b as b_data
import sqlite3

application = Flask(__name__)

data_user = {}
data_step = {}
def get_from_env(key):
    dotenv_path = join(dirname(__file__), '.env')
    load_dotenv(dotenv_path)
    return os.environ.get(key)  # возвращен серкетный токен


def send_message(chat_id, text):
    method = "sendMessage"
    token = get_from_env('TELEGRAM_BOT_TOKEN')
    url = f"https://api.telegram.org/bot{token}/{method}"
    data = {"chat_id": chat_id, "text": text}
    requests.post(url, data=data)

def db_query_ci(q):
    conn = sqlite3.connect("../tgBot/fourstep.sql")
    cursor = conn.cursor()
    cursor.execute(q)
    conn.commit()
    cursor.close()
    conn.close()


def db_query_insert(q, v):
    conn = sqlite3.connect("../tgBot/fourstep.sql")
    cursor = conn.cursor()
    with open('f_err.txt', 'w') as f:
        f.write(f'{q} ---- {type(v)}')
    cursor.execute(q, v)
    conn.commit()
    cursor.close()
    conn.close()


def db_query_select(chat_id, q):
    conn = sqlite3.connect("../tgBot/fourstep.sql")
    cursor = conn.cursor()

    cursor.execute(q)
    users = cursor.fetchall()
    info = ''
    for i in users:
        info += f'{i[5]}\nФамилия: {i[1]}, Имя: {i[2]}, Возраст: {i[3]},Телефон: {i[4]}\n'
    send_message(chat_id, info)
    cursor.close()
    conn.close()

def send_button(chat_id, text, keyboard):
    data_step.clear()
    method = "sendMessage"
    token = get_from_env('TELEGRAM_BOT_TOKEN')
    url = f"https://api.telegram.org/bot{token}/{method}"
    keyboard = {"inline_keyboard": keyboard}
    keyboard = json.dumps(keyboard)
    data = {"chat_id": chat_id, "text": text, "reply_markup": keyboard}
    requests.post(url, data=data)

@application.route("/bot-35", methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        response = request.json
        if 'callback_query' in response:

            chat_id = response['callback_query']["message"]["chat"]["id"]
            data_call = response['callback_query']['data']

            if data_call == 'back_main_menu':
                repl = 'Выберите пожалуйста удобный для Вас филиал: '
                keyboard = b_data.addres_fil_b()
                send_button(chat_id, repl, keyboard)
            elif data_call.startswith('adr_'):
                fill = b_data.address_text(data_call)
                data_user['adres'] = fill
                data_user['adres_call'] = data_call
                text = f'Выберите группу по адресу\n {fill}'
                grupps = b_data.grupp_f()
                keyboard = grupps[data_call]
                keyboard.append([{'text': 'Вернуться в главное меню', 'callback_data': 'back_main_menu'}])
                send_button(chat_id, text, keyboard)
            elif data_call.startswith('fil_'):
                grupp_step = b_data.grupp_text(data_call, data_user['adres_call'])
                data_user['grupp_call'] = data_call
                data_user['grupp'] = grupp_step
                text = f'Введите фамилию ребёнка:\n'
                data_step['step'] = 1
                send_message(chat_id, text)
            return {"ok": True}

        message_ch = response['message']
        chat_id = response["message"]["chat"]["id"]
        text = response["message"]['text']

        if 'entities' in message_ch:
            if text == '/start':
                repl = 'Выберите пожалуйста удобный для Вас филиал: '
                keyboard = b_data.addres_fil_b()
                data_step['step'] = 0
                send_button(chat_id, repl, keyboard)
            elif data_step['step'] == 4:
                data_user['phone'] = text
                text = f"Вы успешно записаны!\n{data_user['adres']}\n{data_user['grupp']}\n{data_user['last_name']} {data_user['first_name']}, возраст: {data_user['old']},\n телефон: {data_user['phone']}"
                data_step['step'] = 5
                queri_1 = f"CREATE TABLE IF NOT EXISTS {data_user['grupp_call']}(id int auto_increment primary key, surname varchar(15), name varchar(15), age varchar(10), phone varchar(20), grupp varchar(30))"
                db_query_ci(queri_1)
                values = (data_user['last_name'], data_user['first_name'], data_user['old'], data_user['phone'], data_user['adres'])
                queri_2 = f"INSERT INTO {data_user['grupp_call']}(surname, name, age, phone, grupp) VALUES(?, ?, ?, ?, ?);"
                db_query_insert(queri_2, values)
                send_message(chat_id, text)
        else:
            if data_step['step'] == 1:
                data_user['last_name'] = text
                text = 'Введите имя ребёнка: '
                data_step['step'] = 2
                send_message(chat_id, text)
            elif data_step['step'] == 2:
                data_user['first_name'] = text
                text = 'Введите возраст ребёнка: '
                data_step['step'] = 3
                send_message(chat_id, text)
            elif data_step['step'] == 3:
                data_user['old'] = text
                text = 'Введите номер своего телефона с кодом мобильного оператора: '
                data_step['step'] = 4
                send_message(chat_id, text)
            elif data_step['step'] == 4:
                data_user['phone'] = text
                text = 'Вы не правильно ввели номер телефона, нужнов формате +375ХХХХХХХХХ'
                send_message(chat_id, text)
                #получение данных
            elif text == 'rokosovskogo1000':
                query = 'SELECT * FROM fil_rokosovskogo_1'
                db_query_select(chat_id, query)
            elif text == 'rokosovskogo1800':
                query = 'SELECT * FROM fil_rokosovskogo_2'
                db_query_select(chat_id, query)
            elif text == 'nalibokskaya1700':
                query = 'SELECT * FROM fil_nalibokskaya_1'
                db_query_select(chat_id, query)
            elif text == 'shugaevo1530':
                query = 'SELECT * FROM fil_shugaevo_1'
                db_query_select(chat_id, query)
            elif text == 'shugaevo1630':
                query = 'SELECT * FROM fil_shugaevo_2'
                db_query_select(chat_id, query)
            elif text == 'zhudro1800':
                query = 'SELECT * FROM fil_zhudro_1'
                db_query_select(chat_id, query)
            elif text == 'mixalovskaya1600':
                query = 'SELECT * FROM fil_mixalovskaya_1'
                db_query_select(chat_id, query)
            elif text == 'mixalovskaya1700':
                query = 'SELECT * FROM fil_mixalovskaya_2'
                db_query_select(chat_id, query)
            elif text == 'ostroshitskaya1600':
                query = 'SELECT * FROM fil_ostroshitskaya_1'
                db_query_select(chat_id, query)
            elif text == 'nikiforova1000':
                query = 'SELECT * FROM fil_nikiforova_1'
                db_query_select(chat_id, query)
            elif text == 'pobeditelei1700':
                query = 'SELECT * FROM fil_pobeditelei_1'
                db_query_select(chat_id, query)
            elif text == 'bratskaya1000':
                query = 'SELECT * FROM fil_bratskaya_1'
                db_query_select(chat_id, query)
            elif text == 'bratskaya1530':
                query = 'SELECT * FROM fil_bratskaya_2'
                db_query_select(chat_id, query)
            elif text == 'bratskaya1630':
                query = 'SELECT * FROM fil_bratskaya_3'
                db_query_select(chat_id, query)
            elif text == 'dzerwinskogo1530':
                query = 'SELECT * FROM fil_odzerwinskogo_1'
                db_query_select(chat_id, query)
            elif text == 'dzerwinskogo1630':
                query = 'SELECT * FROM fil_dzerwinskogo_2'
                db_query_select(chat_id, query)
    else:
        return f'<h1 style="color:blue">Hello, There is BOT!</h1>'
    return {"ok": True}


if __name__ == "__main__":
    application.run(host='0.0.0.0')
