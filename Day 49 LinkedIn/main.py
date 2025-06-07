#--------------This code is going to simulate what would happen if I automated job applications on LinkedIn.-------------#
import selenium.common.exceptions
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
import os
from dotenv import load_dotenv
import time

load_dotenv()

EMAIL_LINKED_IN = os.environ['EMAIL']
PASS_LINKED_IN = os.environ['PASSWORD']

def open_linked_in(email, password):
    print("Setting up Browser and user-profile...")
    url = "https://www.linkedin.com/jobs/search/?currentJobId=4182848300&f_AL=true&geoId=106224388&keywords=python%20developer&origin=JOB_SEARCH_PAGE_JOB_FILTER&refresh=true"
    options = webdriver.ChromeOptions()
    options.add_experimental_option('detach', True)

    # This code ensures that a user profile is made, ensuring the website sees us as HUMAN
    chrome_user_data_dir = os.getenv("CHROME_USER_DATA_DIR")
    if chrome_user_data_dir:
        options.add_argument(f'--user-data-dir={chrome_user_data_dir}')
    else:
        print("Warning: Chrome user data directory not set. Running without user profile.")

    options.add_argument('--profile-directory=SeleniumProfile')

    # Get url
    driver = webdriver.Chrome(options=options)
    driver.get(url=url)
    print("Setup complete!")
    print(f"Checking if signed in using the following url: {url}")

    try:
        # Check for profile menu that only appears when logged in
        driver.find_element(By.XPATH, '//*[@id="ember18"]')  # OR something like "global-nav"
        print("Already signed in! 😎")
        driver.quit()
        return
    except selenium.common.exceptions.NoSuchElementException:
        print("Not signed in, attempting to sign in...")

    # Sign in methods
    try:
        # Sign-in using the button that pops up/MODAL sign in
        sign_in_btn = driver.find_element(by=By.CSS_SELECTOR, value='button.sign-in-modal__outlet-btn')
        sign_in_btn.click()
        email_inp = driver.find_element(by=By.XPATH, value='//*[@id="base-sign-in-modal_session_key"]')
        pass_inp = driver.find_element(by=By.XPATH, value='//*[@id="base-sign-in-modal_session_password"]')
        email_inp.send_keys(f"{email}")
        pass_inp.send_keys(f"{password}", Keys.ENTER)
        print("Signed in successfully! 😎🤖")
        driver.quit()
    except selenium.common.exceptions.NoSuchElementException:
        # Sign-in using the auth wall/FULL PAGE sign-in
        print("Couldn't access it the first time. Signing in to Linked In...")
        # Click SIGN-IN NOT SIGN-UP
        sign_in_btn = driver.find_element(by=By.XPATH, value='//*[@id="main-content"]/div[1]/form/p/button')
        sign_in_btn.click()
        # Click email input and send
        sign_in_email_input = driver.find_element(by=By.XPATH, value='//*[@id="session_key"]')
        sign_in_email_input.click()
        sign_in_email_input.send_keys(f"{email}")
        # Click password inp and send
        sign_in_pass_inp = driver.find_element(by=By.XPATH, value='//*[@id="session_password"]')
        sign_in_pass_inp.click()
        sign_in_pass_inp.send_keys(f"{password}", Keys.ENTER)
        print("Successfully signed in!🥳🎂")
        driver.quit()

def job_handling():
    print("Setting up browser...")
    url = "https://www.linkedin.com/jobs/search/?currentJobId=4182848300&f_AL=true&geoId=106224388&keywords=python%20developer&origin=JOB_SEARCH_PAGE_JOB_FILTER&refresh=true"
    options = webdriver.ChromeOptions()
    options.add_experimental_option('detach', True)

    # This code ensures that a user profile is made, ensuring the website sees us as HUMAN
    options.add_argument(r'--user-data-dir=C:\Users\super\AppData\Local\Google\Chrome\User Data')
    options.add_argument('--profile-directory=SeleniumProfile')

    # Get url
    driver = webdriver.Chrome(options=options)
    driver.set_window_size(1280,1024)
    driver.get(url=url)
    print("Setup complete!")

    wait = WebDriverWait(driver,10)
    saved = 0
    time.sleep(3)

    while saved < 6:
        jobs_list_tag = driver.find_element(by=By.XPATH, value='//*[@id="main"]/div/div[2]/div[1]/div/ul')
        jobs_tags = jobs_list_tag.find_elements(by=By.TAG_NAME, value='li')
        for i in range(len(jobs_tags)):
            try:
                job = jobs_tags[i]
                job.click()
                time.sleep(1)  # Let panel load
                job_title = job.find_element(By.TAG_NAME, 'strong').text
                print(f"Found '{job_title}...")
                save_btn = wait.until(ec.element_to_be_clickable((By.CSS_SELECTOR, "button.jobs-save-button")))
                save_btn.click()
                print(f"Saved: {job_title}")
                saved += 1
                time.sleep(1)
            except Exception as e:
                print(f"Skipping job due to error: {e}")
                continue
# Start the program
print("This program is gonna simulate automated job applications on linked in, WITHOUT actually submitting applications.")
open_linked_in(EMAIL_LINKED_IN, PASS_LINKED_IN)
print("Now that sign in is done, lets save some jobs!")
job_handling()