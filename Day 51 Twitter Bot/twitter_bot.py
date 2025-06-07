from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
import time
import os

EXPECTED_DOWNLOAD_MBPS = 200
EXPECTED_UPLOAD_MBPS = 100
twitter_url = "https://x.com/"
speedtest_url = "https://www.speedtest.net/"

class TwitterBot:
    def __init__(self, email, password):
        # Set up driver and attributes and stuff
        self.driver = None
        self.download_speed = 0
        self.upload_speed = 0
        self.email = email
        self.password = password
        self.get_driver()

    def get_driver(self):
        options = webdriver.ChromeOptions()
        options.add_argument("window-size=1920x1080")
        options.add_argument("--headless")  # <-- this is the key
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        chrome_user_data_dir = os.getenv("CHROME_USER_DATA_DIR")
        if chrome_user_data_dir:
            options.add_argument(f'--user-data-dir={chrome_user_data_dir}')
        else:
            print("Warning: Chrome user data directory not set. Running without user profile.")

        options.add_argument('--profile-directory=SeleniumProfile')

        self.driver = webdriver.Chrome(options=options)

    def get_internet_speed(self):
        url = speedtest_url
        self.driver.get(url=url)
        time.sleep(8) # Wait for page to load
        go_btn = self.driver.find_element(by=By.XPATH, value='//*[@id="container"]/div[1]/div[3]/div/div/div/div[2]/div[3]/div[1]/div[1]/a')
        go_btn.click()
        time.sleep(60) # WAIT FOR PAGE TO GET MY INTERNET SPEED/LOAD

        # Get the download speed and upload speed, change the attributes to that
        download_speed_tag = self.driver.find_element(by=By.CSS_SELECTOR, value='span.download-speed')
        upload_speed_tag = self.driver.find_element(by=By.CSS_SELECTOR, value='span.upload-speed')
        self.download_speed += float(download_speed_tag.text)
        self.upload_speed += float(upload_speed_tag.text)

    def twitter_login(self):
        url = twitter_url
        home_screen = "https://x.com/home"
        self.driver.get(url=url)
        time.sleep(2) # Let page load

        # Sign in
        if self.driver.current_url != home_screen:
            print("Clicking Sign in button and signing in now...")
            sign_in_btn = self.driver.find_element(by=By.XPATH, value='//*[@id="react-root"]/div/div/div[2]/main/div/div/div[1]/div[1]/div/div[3]/div[4]/a')
            sign_in_btn.click()
            time.sleep(2) # Wait
            # Put email
            email_input = self.driver.find_element(by=By.XPATH, value='//*[@id="layers"]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div/div/div/div[4]/label/div/div[2]/div/input')
            email_input.send_keys(self.email, Keys.ENTER)
            time.sleep(2) # Wait
            # HANDLE verification
            self.handle_verification_prompt()
            time.sleep(2)
            # Put pass
            pass_input = self.driver.find_element(by=By.NAME, value='password')
            pass_input.send_keys(self.password, Keys.ENTER)
            time.sleep(7) # Wait and see what happens. Whether twitter loads or shows a captcha or what
            if self.driver.current_url == home_screen:
                print("Logged into X (Twitter) successfully! 🥳🤖 Time to tweet!")
                self.make_tweet(EXPECTED_DOWNLOAD_MBPS, EXPECTED_UPLOAD_MBPS)
            else:
                print("Failed to login to X. (Or maybe there was a Captcha or something?)")
        elif self.driver.current_url == home_screen:
            self.make_tweet(EXPECTED_DOWNLOAD_MBPS, EXPECTED_UPLOAD_MBPS)

    def handle_verification_prompt(self):
        username = 'OlivierSpeed'
        try:
            print("Attempting to handle Twitter verification screen...")
            username_input = self.driver.find_element(By.NAME,
                                                      'text')  # Twitter uses 'text' input for username verification
            username_input.send_keys(username, Keys.ENTER)
            time.sleep(2)
            print("Verification step handled! ✅")
        except Exception as e:
            print("Could not handle verification prompt automatically.")
            print(str(e))

    def make_tweet(self, expected_down, expected_up):
        print("Making tweet right now...")
        wait = WebDriverWait(self.driver, 30)
        tweet_text_btn = wait.until(ec.element_to_be_clickable((By.CSS_SELECTOR, "div[data-testid='tweetTextarea_0']")))

        time.sleep(2)
        # Scroll in into view just in case
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", tweet_text_btn)
        time.sleep(1.5)
        # TWEET (depending on the download n upload speed ofc)
        if self.download_speed < expected_down or self.upload_speed < expected_up:
            tweet_text_btn.click()
            time.sleep(1)
            tweet_text_btn.send_keys(f'Sad day today..., did a speed test on my internet, and I expected AT LEAST '
                                     f'{EXPECTED_DOWNLOAD_MBPS} mbps download and {EXPECTED_UPLOAD_MBPS} mbps upload. '
                                     f'I was given {self.download_speed} mbps download and {self.upload_speed} mbps upload '
                                     f'instead... @ATT lock in :(')
        else:
            tweet_text_btn.click()
            time.sleep(1)
            tweet_text_btn.send_keys(f'GREAT DAY TODAY, did a speed test on my internet, and I expected'
                                     f' {EXPECTED_DOWNLOAD_MBPS} mbps download and {EXPECTED_UPLOAD_MBPS} mbps upload. '
                                     f'I was given {self.download_speed} mbps download and {self.upload_speed} mbps upload!'
                                     f' More than I asked for. Thank the Lord! :D')
        # Post the tweet!
        time.sleep(2)
        post_tweet_btn = wait.until(
            ec.element_to_be_clickable((By.CSS_SELECTOR, "button[data-testid='tweetButtonInline']")))
        post_tweet_btn.click()
        print("Tweet posted! 🚀")