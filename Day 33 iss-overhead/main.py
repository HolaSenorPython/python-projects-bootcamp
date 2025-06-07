import os
import requests
from datetime import datetime
import smtplib
import time
from dotenv import load_dotenv

load_dotenv()  # Loads .env variables

MY_LAT = 33.68175862820573  # Your latitude
MY_LONG = -84.68155977607506  # Your longitude

MY_EMAIL = os.getenv("MY_EMAIL")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
RECEIVER_EMAILS = os.getenv("RECEIVER_EMAILS", "").split(",")  # comma-separated list

def is_close():
    response_iss = requests.get(url="http://api.open-notify.org/iss-now.json")
    response_iss.raise_for_status()
    data_iss = response_iss.json()

    iss_latitude = float(data_iss["iss_position"]["latitude"])
    iss_longitude = float(data_iss["iss_position"]["longitude"])
    
    close = abs(iss_latitude - MY_LAT) <= 5 and abs(iss_longitude - MY_LONG) <= 5
    if not close:
        print("The ISS is not close to us yet.")
    return close

def darkness_check():
    if is_close():
        now = datetime.now()
        if (now.hour > sunset_h or now.hour < sunrise_h) or \
           (now.hour == sunset_h and now.minute >= sunset_min) or \
           (now.hour == sunrise_h and now.minute <= sunrise_min):
            return True
        else:
            print("Noooooo! The ISS is close, but it's too bright to see it!😭😢")
    return False

def send_email():
    if darkness_check():
        with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
            connection.starttls()
            connection.login(user=MY_EMAIL, password=EMAIL_PASSWORD)
            message = "Look up! The ISS is visible from your location!🚀🛰️"
            connection.sendmail(
                from_addr=MY_EMAIL,
                to_addrs=RECEIVER_EMAILS,
                msg=f"Subject:Look up pal🥳\n\n{message}"
            )

parameters = {
    "lat": MY_LAT,
    "lng": MY_LONG,
    "formatted": 0,
}

response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
response.raise_for_status()
data = response.json()

sunrise_h = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
sunrise_min = int(data["results"]["sunrise"].split("T")[1].split(":")[1])
sunset_h = int(data["results"]["sunset"].split("T")[1].split(":")[0])
sunset_min = int(data["results"]["sunset"].split("T")[1].split(":")[1])

print("Starting ISS visibility checker... Press Ctrl+C to stop.")

try:
    while True:
        send_email()
        time.sleep(60)
except KeyboardInterrupt:
    print("\nStopped by user.")
