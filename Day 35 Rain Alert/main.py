import os
import requests
from twilio.rest import Client
from dotenv import load_dotenv

load_dotenv()

# Load from environment
api_key = os.getenv("OWM_API_KEY")
twilio_id = os.getenv("TWILIO_ACCOUNT_SID")
auth_token = os.getenv("TWILIO_AUTH_TOKEN")
from_number = os.getenv("TWILIO_FROM")
to_number = os.getenv("TWILIO_TO")
MY_LAT = float(os.getenv("MY_LAT"))
MY_LNG = float(os.getenv("MY_LNG"))

OWM_ENDPOINT = "https://api.openweathermap.org/data/2.5/forecast"

# Create Twilio client
client = Client(twilio_id, auth_token)

# OpenWeather API request
parameters = {
    "lat": MY_LAT,
    "lon": MY_LNG,
    "appid": api_key,
    "cnt": 4,
}

weather_resp = requests.get(url=OWM_ENDPOINT, params=parameters)
weather_resp.raise_for_status()
weather_data = weather_resp.json()
print(f"Status code: {weather_data['cod']}")

# Check if it will rain
def umbrella_check():
    for d in weather_data["list"]:
        condition_code = d["weather"][0]["id"]
        if condition_code < 700:
            return True
    return False

if umbrella_check():
    message = client.messages.create(
        from_=from_number,
        body="It's going to rain today. Remember to bring an umbrella☔",
        to=to_number
    )
    print(message.status)
else:
    print("You won't need an umbrella today.😎")
