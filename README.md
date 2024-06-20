# AmazonPriceTracker
Price Alert Script
This Python script monitors the price of a specified product on Amazon and sends alerts via email and WhatsApp if the price falls below a certain threshold. The script utilizes Playwright for web scraping, Yagmail for sending emails, and Twilio for sending WhatsApp messages.

Requirements
Python 3.7+
Playwright
Yagmail
Twilio
Environment variables for sensitive information
Installation
Clone the repository:

bash
Copy code
git clone <repository_url>
cd <repository_directory>
Install the required Python packages:

bash
Copy code
pip install playwright yagmail twilio
playwright install
Set up environment variables:

YA_MAIL_SECRET: Yagmail password for the sender email account.
TW_SID: Twilio Account SID.
TW_AUTH_TOKEN: Twilio Auth Token.
These can be set in your operating system or within a .env file.

Configuration
Gmail Credentials:

python
Copy code
sender = "datanewshub@gmail.com"
my_secret = os.environ['YA_MAIL_SECRET']
yag = yagmail.SMTP(user=sender, password=my_secret)
Twilio Credentials:

python
Copy code
account_sid = os.environ['TW_SID']
auth_token = os.environ['TW_AUTH_TOKEN']
client = Client(account_sid, auth_token)
URL and Price Threshold:
Modify the URL and price threshold according to your needs:

python
Copy code
URL = "https://www.amazon.in/Apple-iPhone-15-128-GB/dp/B0CHX1W1XY/"
price_threshold = 80000
Usage
Run the script:

bash
Copy code
python script_name.py
The script will:

Open the specified Amazon product page.
Retrieve the product name and price.
Check if the price is below the threshold.
Send an email and WhatsApp message if the price condition is met.
Wait for 60 seconds and repeat the process.
Code Breakdown
Imports
python
Copy code
import re
from playwright.sync_api import Playwright, sync_playwright, expect
import yagmail
import time
from twilio.rest import Client
import os
Credentials Setup
python
Copy code
# Gmail Credentials
sender = "datanewshub@gmail.com"
my_secret = os.environ['YA_MAIL_SECRET']
yag = yagmail.SMTP(user=sender, password=my_secret)

# Twilio Credentials
account_sid = os.environ['TW_SID']
auth_token = os.environ['TW_AUTH_TOKEN']
client = Client(account_sid, auth_token)
Web Scraping Function
python
Copy code
def run(playwright: Playwright, URL) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto(URL)

    product_name = URL.split('/')[3]
    print(product_name)
    price = page.query_selector("span.a-price-whole").inner_text()

    context.close()
    browser.close()

    return product_name, price
Main Loop
python
Copy code
while True:
    URL = "https://www.amazon.in/Apple-iPhone-15-128-GB/dp/B0CHX1W1XY/"
    with sync_playwright() as playwright:
        product_name, price = run(playwright, URL=URL)

    price = int(price.replace(',', '').replace('.', ''))

    if price <= 80000:
        subject = f"Alert!!! Price of {product_name} is now {price}"
        contents = f"Alert!!! Price of {product_name} is now {price} sent by harish"

        # Sending Mail
        yag.send(to="dewific518@egela.com", subject=subject, contents=contents)
        print("Email Sent!")

        # Sending WhatsApp message
        message = client.messages.create(
            from_='whatsapp:+14155238886',
            body=contents,
            to='whatsapp:+917798125301'
        )

    time.sleep(60)
Notes
Ensure that the Playwright browser drivers are installed correctly.
Make sure the environment variables are set correctly to avoid runtime errors.
Adjust the URL and price threshold as needed.
