from db import admins_col
from telegram import ReplyKeyboardMarkup, Bot, Update
import methods
import state_machine
import admin

def complaint_request(bot: Bot, update: Update):
    update.callback_query.message.reply_text('Опишите жалобу:')
    return state_machine.complain

def complain(bot: Bot, update: Update):
    update.message.reply_text('Жалоба принята')
    admin.log_admin(bot, update.message.text)
    return state_machine.start
