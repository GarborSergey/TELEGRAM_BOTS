import telebot
import requests
import json
from datetime import datetime
from config import currencies

class ConvertionException(Exception):
    pass


class CurrenciesConvertor:

    def handler_message(message: telebot.types.Message):

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
                quote_ticker = get_ticker(quote.title())
                base_ticker = get_ticker(base.title())
                amount = int(amount)

            elif len(values) == 5:
                quote = values[0].title() + ' ' + values[1]
                base = values[2].title() + ' ' + values[3]
                amount = int(values[-1])
                quote_ticker = get_ticker(quote)
                base_ticker = get_ticker(base)

            elif len(values) == 4:
                amount = int(values[-1])
                name = values[0].title() + ' ' + values[1]
                try:
                    quote_ticker = get_ticker(name)
                    quote = name
                    base = values[2].title()
                    base_ticker = get_ticker(base)
                except ConvertionException:
                    name = values[1].title() + ' ' + values[2]
                    base = name
                    quote = values[0].title()
                    quote_ticker = get_ticker(quote)
                    base_ticker = get_ticker(name)

            else:
                raise ConvertionException('Некорректный запрос!')

        except ValueError:
            raise ConvertionException(f'Количество задано некорректно ---> "{values[-1]}"')

        result = {
            'quote': quote,
            'quote_ticker': quote_ticker,
            'base': base,
            'base_ticker': base_ticker,
            'amount': amount,
        }

        return result

    @staticmethod
    def convert(message: telebot.types.Message):
        d = CurrenciesConvertor.handler_message(message)

        if d['quote'] == d['base']:
            raise ConvertionException(f'Невозможно перевести одинаковые валюты {d["base"]}')

        r = requests.get('https://www.cbr-xml-daily.ru/daily_json.js')
        central_bank = json.loads(r.content)
        central_bank['Valute']['RUB'] = {
                "ID": "1",
                "NumCode": "1",
                "CharCode": "RU",
                "Name": "Рубль",
                "Value": 1,
                "Nominal": 1
            }

        refresh_date = datetime.strptime(central_bank['Date'], '%Y-%m-%dT%H:%M:%S%z')
        result = (central_bank['Valute'][d['quote_ticker']]['Value'] * central_bank['Valute'][d['base_ticker']]['Nominal']) / \
                 (central_bank['Valute'][d['base_ticker']]['Value'] * central_bank['Valute'][d['quote_ticker']]['Nominal']) * \
                 d['amount']

        text = f"{d['amount']} {d['quote']} перевести в {d['base']}\n = {result} {d['base']}\n" \
               f"По курсу ЦБ РФ на {refresh_date.strftime('%d.%m.%Y')}"

        return text


