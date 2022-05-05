import telebot
from config import currencies

TOKEN = '5385395435:AAHAJ43C14RngNzgEUcfuE_3K_n9rp5JsNI'


bot = telebot.TeleBot(TOKEN)

# @bot.message_handler()
# def test(message: telebot.types.Message):
#     bot.send_message(message.chat.id, message.text)

@bot.message_handler(commands=['currencies', ])
def currencies_def(message: telebot.types.Message):
    text = 'Перечень доступных валют:\n' \
           '-----------------------------------------\n'

    for currency in currencies:
        text += currencies[currency]['Name'] + '\n'

    text += '-----------------------------------------'
    bot.send_message(message.chat.id, text)

bot.polling(none_stop=True)