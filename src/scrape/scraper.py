import requests
from bs4 import BeautifulSoup

URL = "https://bitinfocharts.com/top-100-richest-bitcoin-addresses.html"


def scrapeWebpage():
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, "html.parser")

    print(soup.prettify())
