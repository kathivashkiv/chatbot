from db import admins_col
from telegram import ReplyKeyboardMarkup, Bot, Update
import methods, state_machine

def add_admin(bot: Bot, update: Update):
    admin = {'admin_id' : update.message.from_user.id}
    f = admins_col.insert_one(admin)

    reply_keyboard=methods.start_keyboard(update)
    update.message.reply_text('Поздравляем, теперь Вы зарегистрированы как админ',
                                reply_markup=ReplyKeyboardMarkup(reply_keyboard))
    return state_machine.start

def log_admin(bot: Bot, text: str):
    for doc in admins_col.find():
        bot.send_message(doc['admin_id'], text)
