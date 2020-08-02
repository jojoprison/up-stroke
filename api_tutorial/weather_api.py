import requests
from api_tutorial.keys import *


url = "https://api.openweathermap.org/data/2.5/weather?q=Moscow&APPID=" + WEATHER_API_KEY

resp = requests.get(url)
print(resp.json())