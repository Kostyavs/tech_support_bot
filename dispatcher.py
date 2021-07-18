import os

from telegram.ext import Updater
from telegram.ext import CommandHandler

import start

updater = Updater(token=os.environ['TOKEN'], use_context=True)
global disp


def start_disp():
    global disp
    disp = updater.dispatcher
    disp.add_handler(CommandHandler('start', start.start))
    disp.add_handler(CommandHandler('help_me', start.help_me))
    disp.add_handler(CommandHandler('new_operator', start.new_operator))
    disp.add_handler(CommandHandler('delete_operator', start.delete_operator))
    return updater
