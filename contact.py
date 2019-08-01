"Sending a tourist contact"
from db import admins_col
from telegram import ReplyKeyboardMarkup, Bot, Update
import methods
import state_machine
import admin

def contact_request(bot: Bot, update: Update, user_data):
    user_data["contact_to_id"] = update.callback_query.data[len('contact'):]
    update.callback_query.message.reply_text('Напишите сообщение с контактной информацией:')
    return state_machine.contact_request

def contact(bot: Bot, update: Update, user_data):
    bot.send_message(user_data["contact_to_id"], text=update.message.text)
    update.message.reply_text('Контактная информация отослана')
    return state_machine.start
