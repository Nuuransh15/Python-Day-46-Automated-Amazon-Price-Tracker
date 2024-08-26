# -------------------- IMPORTS -------------------- #
import os
import requests
from bs4 import BeautifulSoup
import smtplib
from dotenv import load_dotenv

# -------------------- CONSTANTS -------------------- #
PRODUCT_URL = "https://www.amazon.com/dp/B075CYMYK6?ref_=cm_sw_r_cp_ud_ct_FM9M699VKHTT47YD50Q6&th=1"
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
def send_email(product_title: str, product_price: float, url: str):
    """
    Sends an email notification about a product's price drop.
    :param product_title: The title or name of the product that is on sale.
    :param product_price: The current price of the product.
    :param url: The URL where the product can be viewed and purchased.
    :return: None
    """
    # establish smtp connection
    with smtplib.SMTP_SSL(host=os.getenv("GMAIL_SMTP")) as connection:
        connection.login(user=os.getenv("SENDER_EMAIL"), password=os.getenv("SENDER_PASSWORD"))
        subject = "Amazon - Low price alert!"
        body = (f"The item:\"{product_title}\" \n\nis now only \n\n${product_price}\n\nClick here to view "
                f"the item and purchase now: {url}")
        message = f"Subject: {subject}\n\n{body}".encode('utf-8')

        # send low price alert
        connection.sendmail(
            from_addr=os.getenv("SENDER_EMAIL"),
            to_addrs=os.getenv("RECEIVER_EMAIL"),
            msg=message
        )


def price_checker(url: str, headers: dict, target_price: float):
    """
    Checks the price of a product from a given URL and sends an email if the price is lower than the target price.
    :param url: The URL of the product page to scrape for price information.
    :param headers: A dictionary containing headers to be used in the HTTP request (e.g., user-agent).
    :param target_price: The price threshold at which to send a notification.
    :return: None
    """
    # get response
    response = requests.get(url=url, headers=headers)
    webpage_data = response.text

    soup = BeautifulSoup(webpage_data, "html.parser")

    # extract the element containing the price value, remove the currency symbol and convert to float
    product_price = float("".join([soup.find(name="span", class_="aok-offscreen").getText().split("$")[1].strip()]))

    # extract the product name
    product_title = soup.find(name="span", id="productTitle").getText().strip()

    # load environment variables
    load_dotenv()

    # check if price of item is lower than user's target price
    if product_price <= target_price:
        send_email(product_title=product_title, product_price=product_price, url=url)


# -------------------- MAIN EXECUTION -------------------- #
price_checker(url=PRODUCT_URL, headers=HEADERS, target_price=TARGET_PRICE)
