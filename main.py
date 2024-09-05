from bs4 import BeautifulSoup
import requests
from smtplib import SMTP
import os
from os.path import *
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), ".env")
load_dotenv(dotenv_path)
PASSWORD = os.environ.get("password")
MAIL = os.environ.get("my_mail")
TO_MAIL = os.environ.get("to_mail")
header = {
    "Accept-Language": "en-US,en;q=0.9",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",

}
URL = "https://www.amazon.com/dp/B075CYMYK6?psc=1&ref_=cm_sw_r_cp_ud_ct_FM9M699VKHTT47YD50Q6"

response = requests.get(URL, headers=header)
website = response.content
soup = BeautifulSoup(website, "html.parser")
price_whole = soup.find(name="span", class_="a-price-whole").get_text()
price_fraction = soup.find(name="span", class_="a-price-fraction").get_text()
product_title = soup.find(name="span", id="productTitle").get_text().strip()
price = float(price_whole+price_fraction)
MESSAGE = f"Subject:Price drop!!\n\n Hurry up !!\n\t\t{product_title} is now {price}.\n\t\t{URL}"
# print(MESSAGE)
if price < 100:
    with SMTP("smtp.gmail.com", port=587) as connection:
        connection.starttls()
        connection.login(password=PASSWORD, user=MAIL)
        connection.sendmail(from_addr=MAIL,
                            to_addrs=TO_MAIL,
                            msg=MESSAGE.encode("utf-8"))

