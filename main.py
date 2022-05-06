# import bs4
# import io
# from telegram.ext import Updater
# import telegram
# import lxml
# import re
# import requests
# import socket
# import urllib
# import telebot
# import os

# TOKEN = '5312550763:AAEhW6Qbj9TBUW0zQOUThNxpxFGDZ-bsZkY'
# help=""
# bot = telebot.TeleBot(TOKEN);
# @bot.message_handler(content_types=['text'])
# def get_text_messages(message):
#     if message.text == "Привет":
#         bot.send_message(message.from_user.id, "Привет, чем я могу тебе помочь?")
#     if message.text == "help":
#         bot.send_message(message.from_user.id,help)
#     else:
#         bot.send_message(message.from_user.id,message.text)
# # PORT = int(os.environ.get('PORT', '8443'))
# # updater = Updater(TOKEN)
# # # add handlers
# # updater.start_webhook(listen="127.0.0.1",
# #                       port=PORT,
# #                       url_path=TOKEN,
# #                       webhook_url="https://<appname>.herokuapp.com/" + TOKEN)
# # updater.idle()

# # @bot.message_handler(func=lambda message: True, content_types=['text'])
# # def echo_message(message):
# #     bot.reply_to(message, message.text)
# # bot = telebot.TeleBot('5312550763:AAEhW6Qbj9TBUW0zQOUThNxpxFGDZ-bsZkY')
# # Запускаем бота
# bot.polling(none_stop=True, interval=0)
import bs4
import io
import lxml
import re
import requests
import socket
import urllib
