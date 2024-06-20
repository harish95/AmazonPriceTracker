import re
from playwright.sync_api import Playwright, sync_playwright, expect
import yagmail
import time
from twilio.rest import Client
import os


# Gmail Credentials
sender = "datanewshub@gmail.com"

my_secret = os.environ('YA_MAIL_SECRET')

yag = yagmail.SMTP(user=sender, password=my_secret)


# Twilio Credentials
account_sid = os.environ('TW_SID')
auth_token = os.environ('TW_AUTH_TOKEN')


client = Client(account_sid, auth_token)




def run(playwright: Playwright,URL) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto(URL)

    product_name = URL.split('/')[3]
    print(product_name)
    price = page.query_selector("span.a-price-whole").inner_text()

    # ---------------------
    context.close()
    browser.close()

    return product_name,price





while True:

    URL = "https://www.amazon.in/Apple-iPhone-15-128-GB/dp/B0CHX1W1XY/"

    with sync_playwright() as playwright:
        product_name,price = run(playwright, URL=URL)

    price = int(price.replace(',', '').replace('.', ''))

    if price <= 80000:

        subject = f"Alert!!! Price of {product_name} is now {price}"
        contents = f"Alert!!! Price of {product_name} is now {price} sent by harish"

        # Sending Mail
        yag.send(to="dewific518@egela.com", subject=subject, contents=contents)
        print("Email Sent!")

        # Sending whatsapp message
        message = client.messages.create(
        from_='whatsapp:+14155238886',
        body=contents,
        to='whatsapp:+917798125301')


    time.sleep(60)


