import telebot
from config import currencies
from utils import ConvertionException, CurrenciesConvertor
from SF.env.token import TOKEN

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['values', ])
def values(message: telebot.types.Message):
    text = 'Перечень доступных валют:\n' \
           '-----------------------------------------\n'

    for currency in currencies:
        text += currencies[currency]['Name'] + ' ' + currencies[currency]['CharCode']+'\n'

    text += '-----------------------------------------'
    bot.send_message(message.chat.id, text)


@bot.message_handler(commands=['start', ])
def start(message: telebot.types.Message):
    head = '------------------------------------------------------------------\n'
    line_1 = '                      Добро пожаловать!\n'
    line_2 = 'К боту MoneyСhangerGS\n'
    line_3 = 'бот предоставляет возможность\n'
    line_4 = 'перевод одной валюты в другую\n'
    line_5 = 'для получения списка команд введите /help\n'
    line_6 = 'бот использует курсы валют ЦБ РФ\n'
    line_7 = 'https://www.cbr.ru/currency_base/daily/\n'
    bottom = '------------------------------------------------------------------\n'
    footer = 'send me - garborfersru@gmail.com'.center(51)
    text = head + line_1 + line_2 + line_3 + line_4 + line_5 + line_6 + line_7 + bottom + footer
    bot.send_message(message.chat.id, text)


@bot.message_handler(commands=['help', ])
def bot_help(message: telebot.types.Message):
    head = '------------------------------------------------------------------\n'
    line_1 = 'Список команд бота MoneyСhangerGS!\n'
    line_2 = 'для конвертации валюты введите сообщение в следующем формате:\n'
    line_3 = '<валюта, которую хотите перевести> \n'
    line_4 = '<валюта в которую хотите перевести>\n'
    line_5 = '<кол-во>\n'
    line_6 = 'Пример: "Доллар США Рубль 100"\n'
    line_7 = 'Перечень доступных валют /values\n'
    bottom = '------------------------------------------------------------------\n'
    text = head + line_1 + line_2 + line_3 + line_4 + line_5 + line_6 + line_7 + bottom
    bot.send_message(message.chat.id, text)


@bot.message_handler(content_types=['text', ])
def convert(message: telebot.types.Message):

    try:
        text = CurrenciesConvertor.convert(message)
    except ConvertionException as e:
        bot.reply_to(message, f'USER ERROR: \n{e}')
    except Exception as e:
        bot.reply_to(message, f'SERVER ERROR: \n{e}')
    else:
        bot.send_message(message.chat.id, text)


bot.polling(none_stop=True)
