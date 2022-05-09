import telebot
from config import currencies

class ConvertionException(Exception):
    pass


class CurrenciesConvertor:
    @staticmethod
    def split_message(message: telebot.types.Message):

        def get_ticker(name: str):
            for currency in currencies:
                if currencies[currency]['Name'] == name:
                    ticker = currency
                    return ticker
            raise ConvertionException(f'Валюта {name} недоступна')
        pass

    @staticmethod
    def convert():
        pass
