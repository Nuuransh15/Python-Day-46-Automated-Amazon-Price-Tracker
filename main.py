# -------------------- IMPORTS -------------------- #
import requests
from bs4 import BeautifulSoup

# -------------------- CONSTANTS -------------------- #
URL = "https://appbrewery.github.io/instant_pot/"

# -------------------- HELPER FUNCTIONS -------------------- #


# -------------------- MAIN EXECUTION -------------------- #
# get response
response = requests.get(url=URL)
webpage_data = response.text

soup = BeautifulSoup(webpage_data, "html.parser")

# extract the element containing the price value, remove the currency symbol and convert to float
price = float("".join([soup.find(name="span", class_="aok-offscreen").getText().split("$")[1].strip()]))
print(price)

