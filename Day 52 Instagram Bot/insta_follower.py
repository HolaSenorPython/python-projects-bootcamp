from selenium import webdriver
from selenium.common import ElementClickInterceptedException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
import time
import os

INSTA_URL = "https://www.instagram.com/accounts/login/"

class InstaFollower:
    def __init__(self):
        self.driver = None
        self.make_driver()

    def make_driver(self):
        chrome_options = webdriver.ChromeOptions()
        # Keep window open
        chrome_options.add_experimental_option('detach', True)
        # Ensure Chrome is run with our selenium user profile, to prevent any captchas or anything
        chrome_user_data_dir = os.getenv("CHROME_USER_DATA_DIR")
        if chrome_user_data_dir:
            chrome_options.add_argument(f'--user-data-dir={chrome_user_data_dir}')
        else:
            print("Warning: Chrome user data directory not set. Running without user profile.")

        chrome_options.add_argument('--profile-directory=SeleniumProfile')
        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.set_window_size(1280, 1024)

    def insta_login(self, username, password):
        print("Let's try and log in to Instagram...")
        url = INSTA_URL
        self.driver.get(url=url)
        wait = WebDriverWait(self.driver, 10)
        if self.driver.current_url == INSTA_URL:
            print("Instagram Login URL accessed successfully! 🥳")

            # Find the inputs
            username_input = wait.until(ec.presence_of_element_located((By.NAME, 'username')))
            password_input = wait.until(ec.presence_of_element_located((By.NAME, 'password')))

            # Sign-in
            print("Attempting sign-in 🤔...")
            username_input.click()
            username_input.send_keys(username)
            time.sleep(1)
            password_input.click()
            password_input.send_keys(password, Keys.ENTER)
            time.sleep(4)
            # Don't save login info
            dont_save_login_btn = wait.until(ec.presence_of_element_located((By.CSS_SELECTOR, 'div.x1yc6y37')))
            dont_save_login_btn.click()
            if "instagram.com" in self.driver.current_url and "/accounts/login/" not in self.driver.current_url:
                print("Logged onto Instagram successfully! 🚀🤙")
            else:
                print("Failed to login to Instagram. Maybe there's a Captcha, or a popup in the way? 😓")
        elif "instagram.com" in self.driver.current_url and "/accounts/login/" not in self.driver.current_url:
            print("Already signed in! No login necessary! 😅🤙⚔️")
        else:
            print("Something went wrong while trying to access the Instagram url. ❌")

    def find_followers(self):
        target_url = "https://www.instagram.com/freecodecamp/"
        wait = WebDriverWait(self.driver, 15)
        self.driver.get(url=target_url)
        if self.driver.current_url == target_url:
            print("Target Instagram Account acquired successfully! 😏")
        else:
            print("Oops! Something went wrong. Failed to fetch target account. 😿")
        print("Accessing account followers...")
        check_followers_btn = wait.until(ec.presence_of_element_located((By.CSS_SELECTOR, 'a[href="/freecodecamp/followers/"]')))
        check_followers_btn.click()
        print("Account followers popup opened! 🐟")

        print("Waiting for scrollable followers list...")
        time.sleep(2)

        dialog = wait.until(ec.presence_of_element_located((By.XPATH, '//div[@role="dialog"]')))

        # Find all nested divs and debug scrollHeight
        scroll_box = None
        for div in dialog.find_elements(By.TAG_NAME, "div"):
            scroll_height = self.driver.execute_script("return arguments[0].scrollHeight", div)
            client_height = self.driver.execute_script("return arguments[0].clientHeight", div)
            if scroll_height > client_height:
                scroll_box = div
                print(f"FOUND scrollable div: scrollHeight = {scroll_height}, clientHeight = {client_height}")
                self.driver.execute_script("arguments[0].style.border = '3px solid red'", div)
                break

        if scroll_box is None:
            print("❌ Could not find scrollable div inside modal.")
            return

        print("✅ Scrollable box found! Starting scroll...")

        for i in range(10):
            self.follow()
            self.driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", scroll_box)
            print(f"Scrolled {i + 1} time(s)...")

    def follow(self):
        time.sleep(2)
        follow_btns = self.driver.find_elements(by=By.CSS_SELECTOR, value='button._ap30')

        print(f"Found {len(follow_btns)} follow buttons! 🙉")

        for n, follow_btn in enumerate(follow_btns):
            try:
                follow_btn.click()
                print(f"Clicked follow button on user {n + 1}!")
                time.sleep(1)
            except ElementClickInterceptedException:
                print("Oops! We already follow this user 😅! Let's not unfollow.")