import json

import requests
import telebot
from datetime import datetime
from config import currencies
from utils import ConvertionException

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
    def get_ticker(name: str):
        for currency in currencies:
            if currencies[currency]['Name'] == name:
                ticker = currency
                return ticker
        raise ConvertionException(f'Валюта {name} недоступна')

    values = message.text.split()
    try:
        if len(values) == 3:
            quote, base, amount = values
            quote_ticker = get_ticker(quote)
            base_ticker = get_ticker(base)
            amount = int(amount)

        elif len(values) == 5:
            quote = values[0] + ' ' + values[1]
            base = values[2] + ' ' + values[3]
            amount = int(values[-1])
            quote_ticker = get_ticker(quote)
            base_ticker = get_ticker(base)

        elif len(values) == 4:
            amount = int(values[-1])
            name = values[0] + ' ' + values[1]
            try:
                quote_ticker = get_ticker(name)
                quote = name
                base = values[2]
                base_ticker = get_ticker(values[2])
            except ConvertionException:
                name = values[1] + ' ' + values[2]
                base = name
                quote = values[0]
                quote_ticker = get_ticker(values[0])
                base_ticker = get_ticker(name)

        else:
            raise ConvertionException('Некорректный запрос!')

    except ValueError:
        raise ConvertionException(f'Количество задано некорректно ---> "{values[-1]}"')

    r = requests.get('https://www.cbr-xml-daily.ru/daily_json.js')
    central_bank = json.loads(r.content)
    central_bank['Valute']['RUB'] = {
        "ID": "",
        "NumCode": "1",
        "CharCode": "RU",
        "Name": "Рубль",
        "Value": 1,
        "Nominal": 1
    }

    refresh_date = datetime.strptime(central_bank['Date'], '%Y-%m-%dT%H:%M:%S%z')
    result = (central_bank['Valute'][quote_ticker]['Value'] * central_bank['Valute'][base_ticker]['Nominal']) / \
             (central_bank['Valute'][base_ticker]['Value'] * central_bank['Valute'][quote_ticker]['Nominal']) * \
             amount

    text = f'{amount} {quote} перевести в {base}\n === {result} {base}\nПо курсу ЦБ РФ на {refresh_date.strftime("%d %b %Y time:%H:%M")}'

    bot.send_message(message.chat.id, text)


bot.polling(none_stop=True)
