import os
import requests
from datetime import datetime, timedelta
from twilio.rest import Client
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Constants
STOCK_NAME = "AMZN"
COMPANY_NAME = "Amazon"
STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

# Environment-sensitive data
STOCK_API_KEY = os.getenv("STOCK_API_KEY")
NEWS_API_KEY = os.getenv("NEWS_API_KEY")
TWILIO_ID = os.getenv("TWILIO_ID")
TWILIO_TOKEN = os.getenv("TWILIO_TOKEN")
TO_PHONE = os.getenv("TO_PHONE")
FROM_PHONE = os.getenv("FROM_PHONE")

client = Client(TWILIO_ID, TWILIO_TOKEN)

# Fetch stock data
amazon_data_url = (
    f"{STOCK_ENDPOINT}?function=TIME_SERIES_DAILY&symbol={STOCK_NAME}&apikey={STOCK_API_KEY}"
)
response = requests.get(url=amazon_data_url)
response.raise_for_status()
amzn_data = response.json()

# Get dates
today = datetime.now().date()
yesterday = today - timedelta(days=1)
day_before = yesterday - timedelta(days=1)

# --- Helper functions ---
def difference_calc(prev_price, recent_price):
    difference = recent_price - prev_price
    average = (prev_price + recent_price) / 2
    percent_change = (difference / average) * 100
    return round(percent_change, 2)

def get_news():
    news_url = f"{NEWS_ENDPOINT}?q={COMPANY_NAME}&apiKey={NEWS_API_KEY}"
    news_response = requests.get(news_url)
    news_response.raise_for_status()
    articles = news_response.json()["articles"][:3]
    return [(a["title"], a["description"], a["url"]) for a in articles]

def send_message(articles, change):
    arrow = "🔼" if change > 0 else "🔽"
    for title, desc, url in articles:
        msg_body = (
            f"{STOCK_NAME}: {arrow}{abs(change)}%\n"
            f"Headline: {title}\nBrief: {desc}\nArticle: {url}"
        )
        message = client.messages.create(
            from_=FROM_PHONE,
            body=msg_body,
            to=TO_PHONE
        )
        print(f"Message sent: {message.status}")

# --- Main logic ---
try:
    recent_close = float(amzn_data["Time Series (Daily)"][str(yesterday)]["4. close"])
    prev_close = float(amzn_data["Time Series (Daily)"][str(day_before)]["4. close"])
except KeyError:
    refreshed = amzn_data["Meta Data"]["3. Last Refreshed"]
    prev_date = datetime.strptime(refreshed, "%Y-%m-%d").date() - timedelta(days=1)
    recent_close = float(amzn_data["Time Series (Daily)"][refreshed]["4. close"])
    prev_close = float(amzn_data["Time Series (Daily)"][str(prev_date)]["4. close"])

change = difference_calc(prev_close, recent_close)

if abs(change) >= 3:
    articles = get_news()
    send_message(articles, change)
else:
    print("No significant stock change.")
