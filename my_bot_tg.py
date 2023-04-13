from telegram import Bot, ReplyKeyboardMarkup
from telegram.ext import Updater, Filters, MessageHandler, CommandHandler, ConversationHandler
import requests
import datetime
import secret


secret_token = secret.secret_token
chat_id = secret.chat_id

URL_CAT = 'https://api.thecatapi.com/v1/images/search'
URL_DOG = 'https://api.thedogapi.com/v1/images/search'

API_KEY = secret.API_KEY
WEATHER_URL = 'https://api.openweathermap.org/data/2.5/weather'
GEOCODER_URL = 'http://api.openweathermap.org/geo/1.0/direct'
WEATHER_PARAMS = {
    'appid': API_KEY,
    'units': 'metric',
    'lang': 'ru'
}

GEOCODER_PARAMS = {
    'appid': API_KEY
}

bot = Bot(token=secret_token)
updater = Updater(token=secret_token)


def say_hi(update, context):
    chat = update.effective_chat
    context.bot.send_message(chat_id=chat.id,
                             text=f'Привет, {chat.first_name}, я MyTest_bot')
    # update.message.reply_text(f'Привет, {chat.first_name}, я MyTest_bot')
    # return 1


def start(update, context):
    chat = update.effective_chat
    name = chat.first_name
    buttons = ReplyKeyboardMarkup([
        ['/start', '/newcat', '/newdog', '/time', '/weather'],
                                  ], resize_keyboard=True)
    context.bot.send_message(chat_id=chat.id,
                             text=
                             f"""Ку, {name}, чем могу быть полезен? 
Еды пока нет, могу предложить котиков, для этого нажмите на кнопку /newcat, 
или собачек, для этого нажмите на кнопку /newdog, 
чтобы узнать который час нажмите на кнопку  /time, 
чтоб узнать погоду в городе нажмите на кнопку /weather""",
                             reply_markup=buttons
                             )


def stop(update, context):
    chat = update.effective_chat
    name = chat.first_name
    context.bot.send_message(chat_id=chat.id,
                             text=
                             f"""Алибидерчи, {name})"""
                             )


def get_new_image(URL):
    response = requests.get(URL).json()
    return response[0]['url']


def give_new_cat(update, context):
    chat = update.effective_chat
    context.bot.send_photo(chat.id, get_new_image(URL_CAT))


def give_new_dog(update, context):
    chat = update.effective_chat
    context.bot.send_photo(chat.id, get_new_image(URL_DOG))


def time_today(update, context):
    data = datetime.datetime.now()
    time_new = data.time()
    chat = update.effective_chat
    context.bot.send_message(chat_id=chat.id,
                             text=f'Сейчас {time_new}')


def get_city_coords(city):
    GEOCODER_PARAMS['q'] = city
    json = requests.get(GEOCODER_URL, GEOCODER_PARAMS).json()
    lat, lon = json[0]['lat'], json[0]['lon']
    return lat, lon


def print_weather(update, context):
    print(update['message']['text'])
    lat, lon = get_city_coords(update['message']['text'])
    WEATHER_PARAMS['lat'], WEATHER_PARAMS['lon'] = lat, lon
    json = requests.get(WEATHER_URL, WEATHER_PARAMS).json()
    city = json['name']
    description = json['weather'][0]['description']
    temp = json['main']['temp']
    chat = update.effective_chat
    context.bot.send_message(chat_id=chat.id,
                             text=f'Погода в городе: {city}. {description.capitalize()}, температура: {temp} °C.')


def get_weather(update, context):
    chat = update.effective_chat
    context.bot.send_message(chat_id=chat.id,
                             text='Введите город: ')
    updater.dispatcher.add_handler(MessageHandler(Filters.text, print_weather))
    # return 2


# handler = ConversationHandler(
#     entry_points=[CommandHandler('start', start)],
#     states={
#         1: [MessageHandler(Filters.text, say_hi)],
#         2: [MessageHandler(Filters.text, print_weather)]
#     },
#     fallbacks=[CommandHandler('stop', stop)]
# )


def main():
    # updater.dispatcher.add_handler(handler)
    updater.dispatcher.add_handler(CommandHandler('start', start))
    updater.dispatcher.add_handler(CommandHandler('newcat', give_new_cat))
    updater.dispatcher.add_handler(CommandHandler('newdog', give_new_dog))
    updater.dispatcher.add_handler(CommandHandler('time', time_today))
    updater.dispatcher.add_handler(CommandHandler('weather', get_weather))
    # updater.dispatcher.add_handler(MessageHandler(Filters.text, say_hi))
    updater.start_polling()


if __name__ == '__main__':
    main()
