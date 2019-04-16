#!/usr/bin/env python
# -*- coding: utf-8 -*-

import subprocess
import logging
import re
from websocket import create_connection
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

ws = create_connection("ws://localhost:8080/ws")
result =  ws.recv()
print("[TELEGRAM-BOT] WebSocket Received: '%s'" % result)

# Enable logging
logging.basicConfig(format='[TELEGRAM-BOT] %(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments bot and
# update. Error handlers also receive the raised TelegramError object in error.
def start(bot, update):
    """Send a message when the command /start is issued."""
    update.message.reply_text('Hi!')


def help(bot, update):
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help!')


def echo(bot, update):
    re_words = re.compile(u"[\u4e00-\u9fa5]+")
    if re_words.search(update.message.text):
        with subprocess.Popen(['trans', '-b', ':en', update.message.text], stdout=subprocess.PIPE) as proc:
            output, err = proc.communicate()
    else:
        with subprocess.Popen(['trans', '-b', ':zh', update.message.text], stdout=subprocess.PIPE) as proc:
            output, err = proc.communicate()
    reply = output.decode('utf-8').rstrip()
    update.message.reply_text(reply)
    logger.info('{} == {}'.format(update.message.text, reply))
    danmu = 'DANMAKU:{} == {}'.format(update.message.text, reply)
    ws.send(danmu)


def error(bot, update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def main():
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    updater = Updater("710879258:AAGTfR7huwzh9R_Pgtpf9J2gD6ccXfcFzDM")

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))

    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.text, echo))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
