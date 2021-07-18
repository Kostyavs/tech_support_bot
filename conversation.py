from telegram.ext import MessageHandler
from telegram.ext.filters import Filters
from telegram import KeyboardButton
from telegram import ReplyKeyboardMarkup

import db
import dispatcher


def start_conv(update, context):
    text = update.message.text
    text = list(text.split(';'))
    topic = text[1]
    operator = update.message.from_user.id
    db.add_operator(operator, topic)
    client = db.get_client(operator)
    dispatcher.disp.add_handler(MessageHandler(Filters.text & Filters.chat(operator), operator_mes))
    dispatcher.disp.add_handler(MessageHandler(Filters.regex('stop conversation') & Filters.chat(client), stop_conv))
    dispatcher.disp.add_handler(MessageHandler(Filters.text & Filters.chat(client), client_mes))
    keyboard = [KeyboardButton('stop conversation')]
    keyboard = ReplyKeyboardMarkup([keyboard])
    context.bot.send_message(chat_id=client, text='Conversation started. Press \'stop conversation\' button '
                                                  'when your question will be resolved.', reply_markup=keyboard)
    context.bot.send_message(chat_id=operator, text='Conversation started')


def operator_mes(update, context):
    operator = update.message.from_user.id
    client = db.get_client(operator)
    context.bot.send_message(chat_id=client, text=update.message.text)


def client_mes(update, context):
    client = update.message.from_user.id
    operator = db.get_operator(client)
    context.bot.send_message(chat_id=operator, text=update.message.text)


def stop_conv(update, context):
    client = update.message.from_user.id
    operator = db.get_operator(client)
    db.stop_conv(client, operator)
    dispatcher.disp.remove_handler(MessageHandler(Filters.text & Filters.chat(operator), operator_mes))
    dispatcher.disp.remove_handler(MessageHandler(Filters.regex('stop conversation') & Filters.chat(client), stop_conv))
    dispatcher.disp.remove_handler(MessageHandler(Filters.text & Filters.chat(client), client_mes))
    context.bot.send_message(chat_id=operator, text='Conversation stopped')
    context.bot.send_message(chat_id=client, text='See you!')

