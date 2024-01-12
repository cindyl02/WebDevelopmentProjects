from selenium import webdriver
from selenium.webdriver.common.by import By
import time

# Keep Chrome browser open after program finishes
chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)

driver = webdriver.Chrome(options=chrome_options)
driver.get("https://orteil.dashnet.org/experiments/cookie/")

cookie = driver.find_element(By.ID, value="cookie")
items = driver.find_elements(By.CSS_SELECTOR, value="#store div")
item_ids = [item.get_attribute("id") for item in items]

timeout = time.time() + 5
five_min = time.time() + 60 * 5  # 5 minutes

while True:
    while time.time() < timeout:
        cookie.click()

    money = driver.find_element(By.ID, value="money").text
    money = int(money.replace(",", ""))

    available_upgrades = driver.find_elements(By.CSS_SELECTOR, "#store div b")
    affordable_upgrades = {}

    for upgrade in available_upgrades:
        if upgrade.text != "":
            price = int(upgrade.text.split("-")[1].strip().replace(",", ""))
            if price < money:
                affordable_upgrades[price] = upgrade

    most_expensive_upgrade = max(affordable_upgrades)
    affordable_upgrades[most_expensive_upgrade].click()

    timeout = time.time() + 5

    if time.time() > five_min:
        cookies_per_second = driver.find_element(By.ID, "cps").text
        print(cookies_per_second)
        driver.quit()
        break
