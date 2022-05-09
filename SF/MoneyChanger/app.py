import json

import requests
import telebot
from datetime import datetime
from config import currencies
from utils import ConvertionException, CurrenciesConvertor

TOKEN = '5385395435:AAHAJ43C14RngNzgEUcfuE_3K_n9rp5JsNI'

bot = telebot.TeleBot(TOKEN)


# @bot.message_handler()
# def test(message: telebot.types.Message):
#     bot.send_message(message.chat.id, message.text)

@bot.message_handler(commands=['values', ])
def values(message: telebot.types.Message):
    text = 'Перечень доступных валют:\n' \
           '-----------------------------------------\n'

    for currency in currencies:
        text += currencies[currency]['Name'] + '\n'

    text += '-----------------------------------------'
    bot.send_message(message.chat.id, text)


@bot.message_handler(content_types=['text', ])
def convert(message: telebot.types.Message):

    try:
        text = CurrenciesConvertor.convert(message)
    except ConvertionException as e:
        bot.reply_to(message, f'user error: \n{e}')
    except Exception as e:
        bot.reply_to(message, f'bot error: \n{e}')
    else:
        bot.send_message(message.chat.id, text)

bot.polling(none_stop=True)
