from dotenv import load_dotenv
from pprint import pprint
import requests
import os


load_dotenv()

API_KEY = os.getenv("WHEATHER_API_KEY")


def get_weather(city="Kansas City"):

    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}"
    response = requests.get(url).json()

    return response

if __name__ == "__main__":

    city = input("Enter the city name: ")

    if not bool(city.strip()):
        city = "Pune"
    wheater_data = get_weather(city)
    
    if wheater_data["cod"] == '404':

        print("City not found")
    else:
        pprint(wheater_data)
    