# Importing modules
import os
import requests
from apscheduler.schedulers.background import BackgroundScheduler
import telebot

# Global Variables
CITY_NAME = "Delhi,IN"

# Get Telegram Bot Token and Weather API Key from environment variables
BOT_TOKEN = os.getenv('BOT_TOKEN')
WEATHER_API_KEY = os.getenv('WEATHER_API_KEY')

# Check if the environment variables are set
if not BOT_TOKEN or not WEATHER_API_KEY:
    raise ValueError("BOT_TOKEN and WEATHER_API_KEY environment variables must be set")

scheduler = BackgroundScheduler()

# Initialize bot object
bot = telebot.TeleBot(BOT_TOKEN)

def kelvin_to_fahrenheit(kelvin):
    return (kelvin - 273.15) * 9/5 + 32

# Get weather data
def getWeather():
    url = f"https://api.openweathermap.org/data/2.5/weather?q={CITY_NAME}&appid={WEATHER_API_KEY}"
    response = requests.get(url)
    weather_data = response.json()

    weather_text = ""

    if weather_data['cod'] == 200:
        weather_text += f"City : {weather_data['name']}, {weather_data['sys']['country']}\n"
        weather_text += f"Coordinate : {weather_data['coord']['lon']} °N, {weather_data['coord']['lat']} °E\n"
        weather_text += f"Weather : {weather_data['weather'][0]['main']}\n"
        weather_text += f"Temperature : {kelvin_to_fahrenheit(weather_data['main']['temp']):.2f} °F\n"
        weather_text += f"Pressure : {weather_data['main']['pressure']} hPa\n"
        weather_text += f"Humidity : {weather_data['main']['humidity']} %\n"
        weather_text += f"Min-Temp : {kelvin_to_fahrenheit(weather_data['main']['temp_min']):.2f} °F\n"
        weather_text += f"Max-Temp : {kelvin_to_fahrenheit(weather_data['main']['temp_max']):.2f} °F\n"
        weather_text += f"Wind Speed : {weather_data['wind']['speed']} m/s\n"
        weather_text += f"Wind Direction : {weather_data['wind']['deg']}°\n"
        weather_text += f"Visibility : {weather_data['visibility']} m\n"
    else:
        weather_text += f"Error: {weather_data['message']}"

    return weather_text

# Send weather data
def sendWeather(chat_id):
    weather_text = getWeather()
    bot.send_message(
        chat_id,
        text="The current weather details in Delhi are: \n\n" + weather_text
    )

# Start Weather updates
@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Weather updates started successfully.")
    scheduler.add_job(lambda: sendWeather(message.chat.id), 'interval', hours=1)
    scheduler.start()

# Stop weather updates
@bot.message_handler(commands=['stop'])
def stop(message):
    scheduler.remove_all_jobs()
    bot.send_message(message.chat.id, text="Weather updates stopped successfully.")

# Test command
@bot.message_handler(commands=['test'])
def send_welcome(message):
    bot.reply_to(message, "Hello, I am ready to serve you.")
    
# Test command
@bot.message_handler(commands=['boss'])
def send_welcome(message):
    bot.reply_to(message, "Hello, I am vijay who created you")    

# Run the bot
bot.infinity_polling()
