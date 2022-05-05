import json
import requests
from config import keys

class ConvertionException(Exception):
    pass

class CryptoConvertor:
    @staticmethod
    def convert(quote, base, amount):

        if quote == base:
            raise ConvertionException(f'Невозможно перевести одинаковые валюты {base}')

        try:
            base_ticker = keys[base]
        except KeyError:
            raise ConvertionException(f'Невозможно перевести в валюту {base}')

        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise ConvertionException(f'Невозможно перевести валюту {quote}')

        try:
            amount = float(amount)
        except ValueError:
            raise ConvertionException(f'Не удалось обработать количество {amount}')

        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={keys[quote]}&tsyms={keys[base]}')
        total_base = json.loads(r.content)[keys[base]]

        return total_base