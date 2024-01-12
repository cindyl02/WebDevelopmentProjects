import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from config import FORM_URL
import time

ZILLOW_CLONE_URL = "https://appbrewery.github.io/Zillow-Clone/"
headers = {
    "Accept-Language": "en-US,en;q=0.9",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
}

response = requests.get(ZILLOW_CLONE_URL, headers=headers)
zillow_html = response.text

soup = BeautifulSoup(zillow_html, "html.parser")
anchor_tags = soup.find_all(class_="StyledPropertyCardDataArea-anchor")
all_listings = [anchor_tag.attrs["href"] for anchor_tag in anchor_tags]
print(all_listings)

all_prices = soup.find_all(class_="PropertyCardWrapper__StyledPriceLine")
all_prices = [price.text.split("+")[0].split("/")[0] for price in all_prices]
print(all_prices)

all_addresses = soup.find_all(name="address")
all_addresses = [address.text.strip().replace("|", "") for address in all_addresses]
print(all_addresses)

# Keep Chrome browser open after program finishes
chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)

driver = webdriver.Chrome(options=chrome_options)
driver.get(FORM_URL)
time.sleep(5.2)

for n in range(len(all_listings)):
    address_xpath = '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input'
    address_input = driver.find_element(By.XPATH, value=address_xpath)

    address_input.send_keys(all_addresses[n])

    price_xpath = '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input'
    price_input = driver.find_element(By.XPATH, value=price_xpath)

    price_input.send_keys(all_prices[n])

    link_xpath = '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input'
    link_input = driver.find_element(By.XPATH, value=link_xpath)

    link_input.send_keys(all_listings[n])

    time.sleep(2)

    submit_button = driver.find_element(By.XPATH, value="//span[contains(text(), 'Submit')]")
    submit_button.click()

    time.sleep(2)

    submit_another = driver.find_element(By.XPATH, value="//a[contains(text(), 'Submit another response')]")
    submit_another.click()

    time.sleep(2)

driver.quit()
