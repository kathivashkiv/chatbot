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


def start_keyboard(update):
    start_keyboard = ['Сдать', 'Снять']
    merchants_keyboard = ['Поделиться', 'Инфо']
    user = update.message.from_user
    """
    if merchants_col.find_one({'seller_id':user.id}):
        return [merchants_keyboard]
    else:
        keyboard = []
        keyboard.append(merchants_keyboard)
        keyboard.append(start_keyboard)
        return keyboard
        """
    keyboard = []
    keyboard.append(merchants_keyboard)
    keyboard.append(start_keyboard)
    return keyboard

def get_info(bot, update):
    text = """
Этот бот позволяет сдать или снять комнату/квартиру. Чтоб отправить запрос нажмите кнопку "Снять" и
 следуя вопросам бота введите параметры (количество комнат, дату и так далее). Чтобы сдать жилье
 нажмите соответсвенно кнопку "Сдать" и указав город вы зарегистрируетесь и будете получать запросы по
 указаному городу (или по всем городам категории "Другой город")

Сейчас у вас 20 монеток"""

    update.message.reply_text(text)
