from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove,
                InlineKeyboardButton, InlineKeyboardMarkup)
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, RegexHandler,
                          ConversationHandler, CallbackQueryHandler)
import traceback
import time

import request
import state_machine
from db import requests_col, merchants_col
from data import (CATEGORY_1, CATEGORY_2, CITY_1, CITY_2, CITY_3, AMOUNT_1, AMOUNT_2, AMOUNT_3, 
         PERIOD_1, PERIOD_2, PERIOD_3, PRICE_1, PRICE_2, PRICE_3, WHEN_1, WHEN_2, WHEN_3 )

def to_order(bot, update, user_data):
    user_data.clear()
    reply_keyboard = [[CITY_1, CITY_2], [CITY_3, "Другой"]]
    update.message.reply_text('В каком городе?',
                            reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
    return state_machine.city


def input_city(bot, update, user_data):
    user_data['city'] = 'other'
    update.message.reply_text('Введите, пожалуйста, название города:')

def optional_city(bot, update, user_data):
    user_data['optional_city'] = update.message.text

    reply_keyboard = [['1', '2'], ['3', "Другое число"]]
    update.message.reply_text('На сколько комнат?',
                            reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
    return state_machine.rooms

def choose_city(bot, update, user_data):
    user_data['city'] = update.message.text
    
    reply_keyboard = [['1', '2'], ['3', "Другое число"]]
    update.message.reply_text('На сколько комнат?',
                            reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
    return state_machine.rooms


def input_rooms_numb(bot, update, user_data):
    update.message.reply_text('Введите, пожалуйста, количество комнат (число):')

def choose_rooms_numb(bot, update, user_data):
    user_data['rooms'] = update.message.text

    reply_keyboard = [[PERIOD_1, PERIOD_2], [PERIOD_3, "Другой"]]
    update.message.reply_text('Выберите, на какой период:',
                            reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
    return state_machine.period


def input_period(bot, update, user_data):
    update.message.reply_text('Введите, пожалуйста, на какой период:')

def choose_period(bot, update, user_data):
    user_data['period'] = update.message.text
    
    reply_keyboard = [[PRICE_1, PRICE_2], [PRICE_3, "Другой промежуток"]]
    update.message.reply_text('На какую примерную стоимость?',
                            reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
    return state_machine.price



def input_price(bot, update, user_data):
    update.message.reply_text('Введите, пожалуйста, своё число/промежуток:')

def choose_price(bot, update, user_data):
    user_data['price'] = update.message.text
    
    reply_keyboard = [[AMOUNT_1 , AMOUNT_2], [AMOUNT_3, "Ваш вариант"]]
    update.message.reply_text('Сколько человек будет жить?',
                            reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
    return state_machine.amount



def input_amount(bot, update, user_data):
    update.message.reply_text('Введите, пожалуйста, своё число:')

def choose_amount(bot, update, user_data):
    user_data['amount'] = update.message.text
    
    reply_keyboard = [[WHEN_1, WHEN_2], [WHEN_3, 'Ваш вариант']]
    update.message.reply_text('На когда?',
                            reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
    return state_machine.when


def input_when(bot, update, user_data):
    update.message.reply_text('Введите, пожалуйста, свой вариант/число:')

def choose_when(bot, update, user_data):
    user_data['when'] = update.message.text
    user_data['zone'] = ''
    
    reply_keyboard = [['Хочу'], ['Нет, это всё']]
    update.message.reply_text('Хотите уточнить район/улицу?',
                            reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
    return state_machine.zone


def input_zone(bot, update, user_data):
    update.message.reply_text('Введите район/улицу:')

def optional_zone(bot, update, user_data):
    user_data['zone'] = update.message.text

    return confirm_request(bot, update, user_data)

def confirm_request(bot, update, user_data):
    text = "Прочитайте и подтвердите верность Вашего запроса: \n"
    text += request.form_req_message(update, user_data)
    reply_keyboard = [['Верно', 'Ввести наново']]
    update.message.reply_text(text,
                            reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
    return state_machine.confirm_req

