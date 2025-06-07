from insta_follower import InstaFollower
from dotenv import load_dotenv
import os
load_dotenv()

# Grab the env variables
insta_username = os.environ['INSTA_USERNAME']
insta_pass = os.environ['INSTA_PASSWORD']

#---------------THIS IS WHERE THE CODE IS RUN------------------------#
print("Howdy dowdy! This code is gonna use the InstaFollower bot to follow all the "
      "followers of a target account.")

# Initialize a new InstaBot
print("Making new InstaBot...")
insta_bot = InstaFollower()
# Handle Login
insta_bot.insta_login(insta_username, insta_pass)
# Find all of my target account's followers, and follow them, then scroll! (all built in, one method leads to next
insta_bot.find_followers()