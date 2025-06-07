import requests
import datetime as dt
import os
from dotenv import load_dotenv

load_dotenv()

APP_ID = os.environ["NUT_APP_ID"]
APP_KEY = os.environ["NUT_APP_KEY"]
NUTRITIONIX_ENDPOINT = "https://trackapi.nutritionix.com/v2/natural/exercise"
SHEETY_ENDPOINT = os.environ["SHEET_ENDP"]
SHEETY_AUTH = os.environ["SHEET_AUTH"]
WEIGHT = float(os.environ["MY_WEIGHT"])
HEIGHT = float(os.environ["MY_HEIGHT"])
AGE = float(os.environ["MY_AGE"])

exercise_input = input("What exercise(s) did you do today?:\n")

headers = {
    "x-app-id": APP_ID,
    "x-app-key": APP_KEY,
}

exercise_params = {
    "query": exercise_input,
    "weight_kg": WEIGHT,
    "height_cm": HEIGHT,
    "age": AGE,
}
# Nutritionix data
response = requests.post(url=NUTRITIONIX_ENDPOINT,headers=headers,json=exercise_params)
response.raise_for_status()
if response.status_code == 200:
    print(f"Nutritionix API accessed successfully: {response.status_code}")
else:
    print(f"Error accessing Nutritionix API. {response.status_code}")
data = response.json()

# Check if exercise data exists
if not data.get("exercises"):
    print("No exercise data found for your input.⚠️")
    exit()

exercise = data["exercises"][0]
#date and stuff
today = dt.datetime.now()
today_formatted = today.strftime("%d/%m/%Y")
time = today.strftime("%H:%M:%S")

new_row_data = {
    "workout": {
        "date": today_formatted,
        "time": time,
        "exercise": exercise['name'].title(),
        "duration": exercise['duration_min'],
        "calories": exercise['nf_calories'],
    }
}

sheety_headers = {
    "Authorization": SHEETY_AUTH
}

sheet_response = requests.post(url=SHEETY_ENDPOINT, json=new_row_data,headers=sheety_headers)
sheet_response.raise_for_status()
if sheet_response.status_code == 200:
    print(f"Sheety accessed successfully: {sheet_response.status_code}")
else:
    print(f"Error accessing Sheety. {sheet_response.status_code}")

