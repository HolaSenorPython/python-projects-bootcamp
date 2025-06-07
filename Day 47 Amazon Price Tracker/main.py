from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
import html
import smtplib
import os
from dotenv import load_dotenv
from email.mime.text import MIMEText
from email.header import Header
from email.utils import formataddr
INITIAL_PRICE_VALUE = 40.00
load_dotenv()

# Make a request to the webpage, and get the price
def get_price():
    url = "https://www.amazon.com/dp/B083L8RNJR"

    chrome_options = Options()
    # Specify path to Chrome User Data Folder
    chrome_user_data_dir = os.getenv("CHROME_USER_DATA_DIR")
    if chrome_user_data_dir:
        chrome_options.add_argument(f'--user-data-dir={chrome_user_data_dir}')
    else:
        print("Warning: Chrome user data directory not set. Running without user profile.")

    driver = webdriver.Chrome(options=chrome_options)
    driver.get(url=url)

    price_whole_tag = WebDriverWait(driver, 10).until(
        ec.presence_of_element_located((By.XPATH, '//*[@id="corePriceDisplay_desktop_feature_div"]//span[contains(@class, "a-price-whole")]')))
    price_decimal_tag = WebDriverWait(driver, 10).until(
        ec.presence_of_element_located(
            (By.XPATH, '//*[@id="corePriceDisplay_desktop_feature_div"]//span[contains(@class, "a-price-fraction")]'))
    )

    # Parse the TAGS, and get just the price as a float (Note, TAG ABOVE returns '39.99 with savings')
    price_whole = price_whole_tag.text.strip()  # Whole price (e.g. 39)
    price_decimal = price_decimal_tag.text.strip()  # Decimal part (e.g. 99)

    print(f"Whole part: {price_whole}, Decimal part: {price_decimal}")

    if price_whole and price_decimal:
        full_price = f"{price_whole}.{price_decimal}"  # Combine them
        print(f"Full Price: {full_price}")

        # Convert to float
        price_number_value = float(full_price)
        driver.quit()
        return price_number_value
    else:
        print("Price text is empty!")
        driver.quit()
        return None

# Make another request, get the title of product and LINK to product and return tuple
def get_more_info():
    url = "https://www.amazon.com/dp/B083L8RNJR"

    chrome_options = Options()
    # Specify path to Chrome User Data Folder
    chrome_options.add_argument(r'--user-data-dir=C:\Users\super\AppData\Local\Google\Chrome\User Data')
    # This creates the new user I have called SeleniumProfile (this stuff tricks amazon to believing im human)
    chrome_options.add_argument('--profile-directory=SeleniumProfile')
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(url=url)

    product_title_tag = WebDriverWait(driver, 10).until(ec.presence_of_element_located((By.XPATH, '//*[@id="productTitle"]')))

    # Clean up the text
    if product_title_tag:
        print("Product title acquired successfully! 🤯")
        raw_title = product_title_tag.text
        prod_title_formatted = ' '.join(html.unescape(raw_title).split())
        title_n_link = (prod_title_formatted, url)
        driver.quit()
        return title_n_link
    else:
        print("No product tag found on the page.")
        driver.quit()

# Send the email!
def send_email(price_val, title_n_link_tuple):
    stmp_address = os.environ['SMTP_ADDRESS']
    my_email = os.environ['MY_EMAIL']
    my_pass = os.environ['MY_PASSWORD']
    receiver_email = os.environ['RECEIVER_EMAIL']
    print("The price has changed from the initial value! Preparing to send email...")

    title = title_n_link_tuple[0]
    link = title_n_link_tuple[1]
    message = f"{title} is now {price_val}!\nHere is the link to the item: {link}"

    # Encode email using UTF-8, in case of symbols or stuff in product title
    msg = MIMEText(message, _charset='utf-8')
    msg['Subject'] = Header("Amazon Price Change! 🤑🫰", "utf-8")
    msg["From"] = formataddr(("Price Bot", my_email))
    msg["To"] = receiver_email

    # SEND IT!!!
    with smtplib.SMTP(host=stmp_address,port=587) as connection:
        connection.starttls()
        connection.login(user=my_email,password=my_pass)
        connection.sendmail(from_addr=my_email,to_addrs=receiver_email,
                            msg=msg.as_string())

# Let's begin.
print("This program will get data for an item you're tracking price on, and "
      "email you if that item has dropped.")
print("Accessing Amazon...")
product_info_tuple = get_more_info()
if product_info_tuple:
    print(f"The program is currently tracking price of: {product_info_tuple[0]}")
    product_price = get_price()
    if product_price < INITIAL_PRICE_VALUE:
        send_email(product_price, product_info_tuple)
        print("Email sent to inbox! Check your spam folder if you don't see it in your inbox. 🤩")
    else:
        print("The price of this item hasn't dropped below your desired price.")
else:
    print("Failed to retrieve product info.")