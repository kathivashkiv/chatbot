"Sharing and saving requests"
import time
import datetime
from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove,
                InlineKeyboardButton, InlineKeyboardMarkup)
from db import requests_col, merchants_col
import methods
import state_machine
import admin

def share_request(bot, update, user_data):
    req = store_request(update, user_data)
    city = user_data['city']

    text = form_req_message(update, user_data)
    keyboard_markup = answer_keyboard(req)

    admin.log_admin(bot, text)

    for seller in merchants_col.find({'city': city}):   
        bot.send_message(chat_id = seller['seller_id'], text=text, reply_markup=keyboard_markup)

    reply_keyboard=methods.start_keyboard(update)
    update.message.reply_text('Ваш запрос отправлен',
                                reply_markup=ReplyKeyboardMarkup(reply_keyboard))
    return state_machine.start


def store_request(update, user_data):
    request = user_data.copy()
    request['sender'] = update.message.from_user.id

    now = datetime.datetime.utcnow()
    request['time'] = datetime.datetime.now()
    request['number'] = 0
    requests_col.insert_one(request)
    return request

def form_req_message(update, user_data):
    if user_data['city'] == 'other':
        text = user_data['optional_city']
    else:
        text = user_data['city']
    text += ', комнат {} / {} / {} / {} / {}'.format(user_data['rooms'], user_data['period'],
            user_data['price'], user_data['amount'], user_data['when'])

    #change zero zone handling
    if user_data['zone']:
        text += ' / {}'.format(user_data['zone'])
    return text

def answer_keyboard(request):
    keyboard = [[
        InlineKeyboardButton('•Ответить•',
                             callback_data='{}'.format(request['_id'])),
        InlineKeyboardButton('•Пожаловаться•',
                             callback_data='complain{}'.format(request['_id']))]]
    return InlineKeyboardMarkup(keyboard)
