import os
from dotenv import load_dotenv, dotenv_values, find_dotenv 
import telebot
import requests
from io import BytesIO


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
   data = weather["current"] #this is for the current weather only

   weather_message = f"Here it is. \nTemperature: {data["temperature"]} \n{data["weather_descriptions"][0]}" #added [0] to get it from the list
   weather_url = data["weather_icons"][0] #added [0] to get it from the list

   response = requests.get(weather_url)
   weather_image_data = BytesIO(response.content) #.content gets us the raw data instead of url. and BytesIO treats as if it were a real file without saving to hard drive.

   bot.send_photo(message.chat.id, photo=weather_image_data)
   bot.send_message(message.chat.id, weather_message, parse_mode="Markdown")


bot.polling()

