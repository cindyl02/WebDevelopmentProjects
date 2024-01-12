import requests
from bs4 import BeautifulSoup
import smtplib
from config import MY_EMAIL, MY_PASSWORD
import lxml

headers = {
    "Accept-Language": "en-US,en;q=0.9",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
}
URL = "https://www.amazon.ca/Steamer-Clothes-Handheld-Clothing-Capacity/dp/B07HF3X6Y4/ref=sr_1_8?crid=20GW9EXQS3V73&dib=eyJ2IjoiMSJ9.6UNVQXauLNiFV29b1h1DDX1f7CB0aUxH7ID-kdGSzEuWn7C3lj0BEHXM2vNQdpDO9CCPSBHIJFq9TGE9zlYeriErSQBk0ueeL_P74SfiabQ9DgZ7LNM1o5kHbejfTSVXZHlBpJopt6zDkMvd3Z5JtJ02s0KF-s-QO-RP-JXbbSat447e--4rizFsLqtYnImGfDBW1NOOCpwnTA4rCRenFmfw2PQWJkUO7xQrOGC1i1A.gtfAU1NKbXxkGay4P_GyYpgBv3PJpAENLJNLomHE1nk&dib_tag=se&keywords=steamer&qid=1705373173&refinements=p_72%3A11192170011&rnid=11192166011&sprefix=steamer%2Caps%2C149&sr=8-8&th=1"

response = requests.get(url=URL, headers=headers)
product_html = response.text

soup = BeautifulSoup(product_html, "lxml")
price = soup.find(class_="a-offscreen").getText()
price = float(price.split("$")[1])

product_name = soup.find(name="span", id="productTitle").getText().strip()

TARGET_PRICE = 30

if price < TARGET_PRICE:
    with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
        connection.starttls()
        connection.login(user=MY_EMAIL, password=MY_PASSWORD)
        connection.sendmail(
            from_addr=MY_EMAIL,
            to_addrs=TO_EMAIL,
            msg=f"Subject:Amazon Price Alert!\n\n{product_name} is now ${price}\n{URL}.".encode("utf8")
        )
