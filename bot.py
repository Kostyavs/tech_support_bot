import logging
import os

from telegram.ext import Updater
from telegram.ext import CommandHandler

import dispatcher

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

updater = dispatcher.start_disp()

updater.start_polling()
