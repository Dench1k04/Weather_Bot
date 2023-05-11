import telegram
import requests

# Enter YOUR_BOT_TOKEN with your bot's token
bot = telegram.Bot(token='YOUR_BOT_TOKEN')

# Enter your OpenWeatherMap API key
url = 'http://api.openweathermap.org/data/2.5/weather?q={},{}&units=metric&appid=YOUR_OPENWEATHERMAP_API_KEY'

def get_weather(update, context):
    location = update.message.text.split(' ')[1:]
    if not location:
        context.bot.send_message(chat_id=update.effective_chat.id, text='Please specify a location.')
        return
    location = ' '.join(location)
    response = requests.get(url.format(location, ''))
    if response.status_code != 200:
        context.bot.send_message(chat_id=update.effective_chat.id, text='Unable to get weather information for {}.'.format(location))
        return
    data = response.json()
    weather_description = data['weather'][0]['description']
    temperature = data['main']['temp']
    feels_like = data['main']['feels_like']
    message = 'Current weather in {}: {} ({}°C, feels like {}°C)'.format(location, weather_description, temperature, feels_like)
    context.bot.send_message(chat_id=update.effective_chat.id, text=message)

from telegram.ext import CommandHandler
updater = Updater(token='YOUR_BOT_TOKEN', use_context=True)
dispatcher = updater.dispatcher
dispatcher.add_handler(CommandHandler('weather', get_weather))
updater.start_polling()
