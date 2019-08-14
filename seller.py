from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove, Bot, Update,
                InlineKeyboardButton, InlineKeyboardMarkup, InputMediaPhoto)
import pymongo
from bson.objectid import ObjectId

import state_machine
import methods
import complaint
import contact
import request
from db import requests_col, merchants_col
from data import CITY_1, CITY_2, CITY_3

def to_lease(bot, update, user_data):
    user_data.clear()
    reply_keyboard = [[CITY_1, CITY_2], [CITY_3, 'Другие']]
    update.message.reply_text('По какому городу хотите получать запросы?',
                            reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
    return state_machine.seller_city

def input_seller_city(bot, update, user_data):
    user_data['city'] = 'other'
    update.message.reply_text('Введите свой город:')
    return state_machine.opt_sell_city

def optional_seller_city(bot, update, user_data):
    user_data['optional_city'] = update.message.text
    register_seller(bot, update, user_data)
    return state_machine.start

def choose_seller_city(bot, update, user_data):
    user_data['city'] = update.message.text
    register_seller(bot, update, user_data)
    return state_machine.start

def register_seller(bot, update, user_data):
    seller = user_data.copy()
    seller['seller_id'] = update.message.from_user.id

    seller['coins'] = 20
    merchants_col.insert_one(seller)

    reply_keyboard=methods.start_keyboard(update)
    update.message.reply_text('Поздравляем, теперь Вы зарегестрированы',
                                reply_markup=ReplyKeyboardMarkup(reply_keyboard))


def to_answer(bot, update, user_data):
    user_data.clear()
    query = update.callback_query
    if query.data.startswith('complain'):
        return complaint.complaint_request(bot, update)
    elif query.data.startswith('contact'):
        return contact.contact_request(bot, update, user_data)
    else:
        req_id = query.data
        user_data['answer_to'] = requests_col.find_one({'_id':ObjectId(req_id)})['sender']
        user_data['answer_req'] = query.message.message_id
    reply_keyboard = [['1', '2'], ['3', "Ваше количество"]]
    query.message.reply_text('Опишите Ваше предложение:\nСколько комнат?',
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
    return state_machine.var_rooms

def var_repeat(bot, update, user_data):
    reply_keyboard = [['1', '2'], ['3', "Ваше количество"]]
    update.message.reply_text('Опишите Ваше предложение:\nСколько комнат?',
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
    return state_machine.var_rooms

def input_rooms_numb(bot, update, user_data):
    update.message.reply_text('Введите, пожалуйста, количество комнат (число):')

def choose_rooms_numb(bot, update, user_data):
    user_data['rooms'] = update.message.text

    update.message.reply_text('Укажите, когда свободный:')
    return state_machine.var_period

def input_period(bot, update, user_data):
    user_data['period'] = update.message.text

    update.message.reply_text('Укажите цену:')
    return state_machine.var_price

def input_price(bot, update, user_data):
    user_data['price'] = update.message.text

    update.message.reply_text('Введите описание (адрес, дополнительные плюсы):')
    return state_machine.var_description

def input_description(bot, update, user_data):
    user_data['description'] = update.message.text

    user_data['photo'] = []
    user_data['url'] = ''
    update.message.reply_text('Прикрепите фото или ссылку на ваше предложение:')
    return state_machine.var_photo

def input_photo(bot, update, user_data):
    user_data['photo'].append(update.message.photo)
    confirm(bot, update, user_data)
    return state_machine.var_confirm

def input_url(bot, update, user_data):
    user_data['url'] = update.message.text
    confirm(bot, update, user_data)
    return state_machine.var_confirm

def confirm(bot, update, user_data):
    text = text = "Прочитайте и подтвердите верность Вашего ответа: \n" + form_answer(user_data)
    reply_keyboard = [['Верно', 'Ввести наново']]
    mess = update.message.reply_text(text,
                            reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
    if len(user_data['photo']) == 1:
        bot.send_photo(chat_id=user_data['answer_to'],
                       photo=user_data['photo'][0][0].file_id,
                       reply_to_message_id=mess.message_id)

def form_answer(user_data):
    text = 'Есть вариант\nКомнат {}, свободно {}, цена {}, описание:\n{}\n' \
            .format(user_data['rooms'], user_data['period'],
                    user_data['price'], user_data['description'])
    if user_data['url']:
        text += 'ссылка: {}'.format(user_data['url'])
    return text

def send_answer(bot, update: Update, user_data):
    text = form_answer(user_data)
    
    keyboard = InlineKeyboardMarkup([[
        InlineKeyboardButton('•Контакт•',
                             callback_data='contact{}'.format(update.message.from_user.id)),
        InlineKeyboardButton('•Пожаловаться•',
                             callback_data='complain{}'.format(update.message.from_user.id))]])

    mess = bot.send_message(chat_id=user_data['answer_to'], text=text, reply_markup=keyboard)
    if len(user_data['photo']) == 1:
        bot.send_photo(chat_id=user_data['answer_to'],
                       photo=user_data['photo'][0][0].file_id,
                       reply_to_message_id=mess.message_id)
    """elif len(user_data['photo'])>=2 :
        #import ipdb; ipdb.set_trace()
        photos=[]
        for obj in user_data['photo']:
            file_id = obj[0].file_id
            photos.append(InputMediaPhoto(media=file_id))
        bot.send_media_group(chat_id=user_data['answer_to'],
                            media=photos, reply_to_message_id=mess.message_id)
    """
    keyboard = InlineKeyboardMarkup([[
        InlineKeyboardButton('•Отвечено•', callback_data='done')]])
    bot.edit_message_reply_markup(chat_id=update.message.from_user.id,
                            message_id=user_data['answer_req'],
                            reply_markup=keyboard)
    
    reply_keyboard = methods.start_keyboard(update)
    update.message.reply_text('Ответ отправлен',
                              reply_markup=ReplyKeyboardMarkup(reply_keyboard))
    return state_machine.start

def user_account(bot, update, user_data):
    user = merchants_col.find({ 'seller_id' : update.message.from_user.id})
    text = ""
    for doc in list(user):
        text += get_city_and_coins(doc)
   
    reply_keyboard = methods.start_keyboard(update)
    update.message.reply_text(text,
                              reply_markup=ReplyKeyboardMarkup(reply_keyboard))
    return state_machine.start 

def get_city_and_coins(seller):
    if (seller['city'] != 'other')  :
        city = seller['city']
    else : city = seller['optional_city'] 
    text = "\nВи зарегестрированы в городе {}".format(city)
    
    if 'coins' in seller:
        coins = seller['coins']
    else : coins = 0
    text += "\nНа счету {} монеток\n".format(coins)
    return text