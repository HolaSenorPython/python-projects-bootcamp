import smtplib
import datetime as dt
import random
from dotenv import load_dotenv
import os

# Load .env variables
load_dotenv()

# Get environment variables
MY_EMAIL = os.getenv("MY_EMAIL")
MY_EMAIL_PASS = os.getenv("MY_EMAIL_PASS")
TO_EMAIL = os.getenv("TO_EMAIL")

# Get base path of this script for relative paths
BASE_PATH = os.path.dirname(os.path.abspath(__file__))
quotes_path = os.path.join(BASE_PATH, "quotes.txt")

now = dt.datetime.now()
day_of_week = now.weekday()

list_of_q = []

def send_email():
    with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
        connection.starttls()
        connection.login(user=MY_EMAIL, password=MY_EMAIL_PASS)
        message = f"Subject:Motivational Sunday\n\n{random_quote}\n\nBe happy today!"
        connection.sendmail(from_addr=MY_EMAIL, to_addrs=TO_EMAIL, msg=message.encode("utf-8"))

with open(quotes_path, "r", encoding="utf-8") as quotes_file:
    quotes = quotes_file.readlines()
    for quote in quotes:
        list_of_q.append(quote.strip())
    random_quote = str(random.choice(list_of_q))
    if day_of_week == 6:
        send_email()
