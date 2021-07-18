from telegram.ext import MessageHandler
from telegram.ext.filters import Filters
from telegram import KeyboardButton
from telegram import ReplyKeyboardMarkup

import dispatcher
import db
import conversation


def start(update, context):
    context.bot.send_message(chat_id=update.message.from_user.id,
                             text='Hi! If you have any questions, just send /help_me')


def create_topic(update, context):
    client_name = update.message.from_user.username
    client_id = update.message.from_user.id
    topic = update.message.text
    dispatcher.disp.remove_handler(topic_handler)
    db.add_topic(client_name, client_id, topic)
    context.bot.send_message(chat_id=client_id, text='Cool! Please wait until operator answer to you.')

    operators = db.get_operators()
    conversations = db.get_conversations()
    keyboard = []
    #print('conversations1: ', conversations)
    for conv in conversations:
        button = ';'.join(map(str, conv))
        dispatcher.disp.add_handler(MessageHandler(Filters.text(button), conversation.start_conv))
        keyboard.append([KeyboardButton(button)])
    print('keyboard: ', keyboard)
    conv_keyboard = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    for operator in operators:
        context.bot.send_message(chat_id=operator, text='Client asked for support', reply_markup=conv_keyboard)


topic_handler = MessageHandler(Filters.text, create_topic)


def help_me(update, context):
    if db.check_client(update.message.from_user.id):
        context.bot.send_message(chat_id=update.message.from_user.id, text='You already asked for support')
    else:
        context.bot.send_message(chat_id=update.message.from_user.id, text='Type your problem, and I\'ll call operator')
        dispatcher.disp.add_handler(topic_handler)

def new_operator(update, context):
    name = update.message.from_user.username
    id = update.message.from_user.id
    db.new_operator(name, id)
    context.bot.send_message(chat_id=id, text='Successfully added!')


def delete_operator(update, context):
    id = update.message.from_user.id
    db.delete_operator(id)
    context.bot.send_message(chat_id=id, text='Successfully deleted!')


def clear_db(update, context):
    db.clear_all()
    context.bot.send_message(chat_id=id, text='Successfully deleted!')
