# -------------------- IMPORTS -------------------- #
import os
import requests
from bs4 import BeautifulSoup
import smtplib
from dotenv import load_dotenv

# -------------------- CONSTANTS -------------------- #
URL = "https://www.amazon.com/dp/B075CYMYK6?ref_=cm_sw_r_cp_ud_ct_FM9M699VKHTT47YD50Q6&th=1"
TARGET_PRICE = 99.99  # $ dollars
HEADERS = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng"
              ",*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8",
    "Sec-Ch-Ua": "\"Not)A;Brand\";v=\"99\", \"Google Chrome\";v=\"127\", \"Chromium\";v=\"127\"",
    "Sec-Ch-Ua-Mobile": "?0",
    "Sec-Ch-Ua-Platform": "\"Windows\"",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "cross-site",
    "Sec-Fetch-User": "?1",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/127.0.0.0 Safari/537.36",
}
# -------------------- HELPER FUNCTIONS -------------------- #


# -------------------- MAIN EXECUTION -------------------- #
# get response
response = requests.get(url=URL, headers=HEADERS)
webpage_data = response.text

soup = BeautifulSoup(webpage_data, "html.parser")

# extract the element containing the price value, remove the currency symbol and convert to float
product_price = float("".join([soup.find(name="span", class_="aok-offscreen").getText().split("$")[1].strip()]))

# extract the product name
product_title = soup.find(name="span", id="productTitle").getText().strip()

# load environment variables
load_dotenv()

# check if price of item is lower than user's target price
if product_price <= TARGET_PRICE:

    # establish smtp connection
    with smtplib.SMTP_SSL(host="smtp.gmail.com") as connection:
        connection.login(user=os.getenv("SENDER_EMAIL"), password=os.getenv("SENDER_PASSWORD"))
        subject = "Amazon - Low price alert!"
        body = f"{product_title} is now ${product_price}\nClick here to view and purchase now: {URL}"
        message = f"Subject: {subject}\n\n{body}".encode('utf-8')

        # send low price alert
        connection.sendmail(
            from_addr=os.getenv("SENDER_EMAIL"),
            to_addrs=os.getenv("RECEIVER_EMAIL"),
            msg=message
        )
