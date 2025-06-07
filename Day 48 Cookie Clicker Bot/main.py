from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import os
from dotenv import load_dotenv

# Keep browser open at MY command >:D
chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option('detach', True)

chrome_user_data_dir = os.getenv("CHROME_USER_DATA_DIR")
if chrome_user_data_dir:
    chrome_options.add_argument(f'--user-data-dir={chrome_user_data_dir}')
else:
    print("Warning: Chrome user data directory not set. Running without user profile.")
# This creates the new user I have called SeleniumProfile
chrome_options.add_argument('--profile-directory=SeleniumProfile')

# Grab the cookie clicker link
driver = webdriver.Chrome(options=chrome_options)
driver.get("https://orteil.dashnet.org/experiments/cookie/")

# Grab the cookie and click!
cookie = driver.find_element(by=By.ID, value='cookie')

# Set up timer
start_time = time.time() # Dynamic, gets updated in while loop
click_duration = 5 # seconds
pause_duration = 1 # second
total_time = 300 # seconds (5 minutes)
another_timer = time.time() # NOT dynamic, value doesn't change in while loop

def is_five_min(seconds): # checks in its 5 minutes
    global another_timer
    time_rn = time.time()
    time_passed = int(time_rn - another_timer)
    if time_passed >= seconds:
        return True
    elif time_passed < seconds:
        return False

# Track time and execute code!
while not is_five_min(total_time):
    current_time = time.time() # Current time RIGHT NOW in loop
    elapsed_time = int(current_time - start_time) # Elapsed time is time NOW minus whatever start is

    if elapsed_time < click_duration: # If it's been less than 5 seconds, click
        cookie.click() # Click at an insane rate
    elif elapsed_time < click_duration + 3: # If it's less than 8 seconds (5 + 3), buy something in store
        user_money = int(driver.find_element(by=By.ID, value='money').text) # Grab how much money we have
        for number in range(10): # 10 store items
            try:
                store_items = driver.find_elements(by=By.CSS_SELECTOR, value='div#store div')  # grab the store items
                store_items = [item for item in store_items if 'buyElder Pledge' not in item.get_attribute("id")]  # Make the store items list not include that deprecated/hidden item
                store_items.reverse()  # REVERSE ORDER, they are from LEAST to GREATEST ORIGINALLY, so SWITCH IT!

                item = store_items[number]
                item_cost_tag = item.find_element(by=By.TAG_NAME, value='b') # get that item's tag
                item_text = item_cost_tag.text  # Get the text
                item_parts = item_text.split(" - ") # Split it into item name and price
                item_cost = int(item_parts[1].strip().replace(",", "")) # remove any commas and spaces, and convert to int
                if user_money >= item_cost:
                    item.click()
                    print(f"Bought {item_parts[0]} for {item_parts[1]} Cookies!")
                    break
            except Exception as e:
                print(f"Something went wrong: {e}")
    else:
        start_time = time.time() # If 8 seconds have passed, the new start time is the time NOW / RESET

# After while loop is finished / AFTER 5 MINUTES
print("Bot shutting down.✌️Be on the lookout for your score!")

if is_five_min(total_time):
    try:
        cookies_per_sec_tag = driver.find_element(by=By.XPATH, value='//*[@id="cps"]')
        cps_text = cookies_per_sec_tag.text
        print(f"Final Cookies per second ratio: {cps_text}")
    except Exception as e:
        print(f"Couldn't retrieve CPS: {e}")