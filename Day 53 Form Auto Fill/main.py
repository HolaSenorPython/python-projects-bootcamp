from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
import requests
import time
import re
import os
from dotenv import load_dotenv


load_dotenv()

FORMS_LINK = "https://forms.gle/Z429UtUy8iY2GnMc6"
ZILLOW_CLONE_LINK = "https://appbrewery.github.io/Zillow-Clone/"


def get_property_info():
    properties = []
    url = ZILLOW_CLONE_LINK
    response = requests.get(url=url)
    response.raise_for_status()
    # Tell me if it was successful access
    if response.status_code == 200:
        print("Zillow site accessed successfully!")
    zillow_webpage = response.text
    soup = BeautifulSoup(zillow_webpage, 'html.parser')
    # Find all the property tags FIRST, and then tell me if successful
    property_tags = soup.find_all(name='div', class_='StyledPropertyCardDataWrapper')
    if property_tags:
        print("Property tags found!")
    # Now, in those property tags, get the link, address, and price
    for property_tag in property_tags:
        link_and_address_tag = property_tag.find(name='a')
        address_tag = link_and_address_tag.find(name='address')
        price_tag_div = property_tag.find(name='div', class_='PropertyCardWrapper')
        price_tag = price_tag_div.find(name='span')
        link = link_and_address_tag.get('href')
        address = address_tag.string.strip()
        price_unformatted = price_tag.string
        price = re.sub(r"\+?\d*\s*bd|/mo|\+", "", price_unformatted).strip()
        property_info = (address, price, link)
        properties.append(property_info)
    return properties

def fill_out_google_form(property_list):
    print("let's get ready to fill out the Google form! Setting up browser first...")
    url = FORMS_LINK # See forms link at the TOP of the code
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_experimental_option('detach', True)
    # Ensure Chrome is run with our selenium user profile, to prevent any captchas or anything
    chrome_user_data_dir = os.getenv("CHROME_USER_DATA_DIR")
    if chrome_user_data_dir:
        chrome_options.add_argument(f'--user-data-dir={chrome_user_data_dir}')
    else:
        print("Warning: Chrome user data directory not set. Running without user profile.")
    chrome_options.add_argument('--profile-directory=SeleniumProfile')
    # Make driver
    driver = webdriver.Chrome(options=chrome_options)
    driver.set_window_size(1280,1024)
    driver.get(url=url)

    # Start the process! Let's check if we're here first...
    if 'docs.google.com' in driver.current_url:
        print("Google Forms successfully accessed! 😏")
        # If we're here, get the questions (the input tags)
        questions = driver.find_elements(by=By.CSS_SELECTOR, value='input.zHQkBf')
        if questions:
            print("Questions found!😁 Filling them out now...")
        else:
            print("Couldn't find the questions (which means i couldn't answer them. 😓😿")
            return
        time.sleep(2)
        for property_info_tuple in property_list:
            # Re-fetch ALL the questions to avoid stale elements
            questions = driver.find_elements(by=By.CSS_SELECTOR, value='input.zHQkBf')
            # Define the different question types (price, link, address)
            address_q = questions[0]
            price_q = questions[1]
            link_q = questions[2]
            # decipher the address, price, and link in every tuple in that list
            address = property_info_tuple[0]
            price = property_info_tuple[1]
            link = property_info_tuple[2]
            # Click on address question, and send the keys
            address_q.click()
            address_q.send_keys(address)
            time.sleep(1)
            # Click on price question, and send the keys
            price_q.click()
            price_q.send_keys(price)
            time.sleep(1)
            # Click on link question, and send the keys
            link_q.click()
            link_q.send_keys(link)

            # Get the submit form button and click
            submit_form_button = driver.find_element(by=By.CSS_SELECTOR, value='div.QvWxOd')
            submit_form_button.click()
            print(f"Google form number {property_list.index(property_info_tuple) + 1} submitted!")

            # Get the submit NEW response form and do it all again
            submit_new_response_btn = driver.find_element(by=By.XPATH, value='/html/body/div[1]/div[2]/div[1]/div/div[4]/a')
            submit_new_response_btn.click()
            time.sleep(2) # Wait for new page to load
    else:
        print("Failed to fetch Google form. 😓")
        return

# Lets Begin!
print("Yoooo! 😎 This code is going to scrape an App Brewery Zillow Clone for San Francisco Properties,\n"
      "Get their information (such as prices and hyperlinks), and fill out a google form for each of them.")
print("Let's gooooo!! 😴😴")
# Get property Info
properties_list = get_property_info()
print(properties_list)
# Fill out the forms!
fill_out_google_form(property_list=properties_list)