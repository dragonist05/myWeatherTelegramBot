import os
from dotenv import load_dotenv, dotenv_values, find_dotenv 
import telebot
import requests


load_dotenv()
#Token for bot
BOT_TOKEN = os.getenv('BOT_TOKEN')
bot = telebot.TeleBot(BOT_TOKEN)

#API key
API_KEY = os.getenv('KEY')

#Getting the weather data from API
def generateWeather(querystring):
 url = f"https://api.weatherstack.com/current?access_key={API_KEY}"
 params = {"query": querystring}
 response = requests.get(url, params)
 return response.json()



# Handler for the /start command
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Use /weather to learn weather!")

#Handler for location
@bot.message_handler(commands=['weather'])
def location_handler(message):
    location = bot.send_message(message.chat.id, "Please enter your location", parse_mode="Markdown") #get user input
    bot.register_next_step_handler(location, fetchWeather)


def fetchWeather(message): #fetch the weather data
   location = message.text
   weather = generateWeather(location)
   data = weather["current"]
   weather_message = f"Here it is. \nTemperature: {data["temperature"]} \n{data["weather_descriptions"]}"
   weather_image = data["weather_icons"] #will add bot to send photo 


   bot.send_message(message.chat.id, weather_message, parse_mode="Markdown")


bot.polling()

