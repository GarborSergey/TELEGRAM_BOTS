import telebot

TOKEN = "5378812654:AAG5r_OGBb4vR98W96Hc9DhuGVkam2uTYlc"

bot = telebot.TeleBot(TOKEN)

# @bot.message_handlers(commands=['start', 'help'])
# def handle_start_help(message):
#     pass

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message: telebot.types.Message):
    bot.send_message(message.chat.id, f'Zdarova! {message.chat.username}')

@bot.message_handler(content_types=['photo', ])
def handle_photo(message: telebot.types.Message):
    bot.reply_to(message, 'nice photo!')

bot.polling(none_stop=True)