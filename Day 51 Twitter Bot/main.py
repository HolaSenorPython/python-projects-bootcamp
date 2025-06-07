# This is MAIN FILE, will do the stuff in the class
from dotenv import load_dotenv
import os
from twitter_bot import TwitterBot

load_dotenv()
TWITTER_EMAIL = os.environ['EMAIL']
TWITTER_PASS = os.environ['PASSWORD']

print("Hey! This code will make a new twitter bot object from the class created, \n"
      "and depending on our internet speed, tweet something!")

# Make a new Twitter bot object
print("Lets begin! Making a new TwitterBot object...")
twitter_bot = TwitterBot(TWITTER_EMAIL, TWITTER_PASS)

# Get the internet speed
print("Object made! Grabbing internet speed using TwitterBot...")
print("(NOTE: This will take around a minute to complete. Please be patient!😅)")
twitter_bot.get_internet_speed()
print("Done! 😎")
print(f"Download Speed: {twitter_bot.download_speed} mbps")
print(f"Upload Speed: {twitter_bot.upload_speed} mbps")

# Tweet!
print("Time to access Twitter and tweet! Handling that now...")
twitter_bot.twitter_login()

