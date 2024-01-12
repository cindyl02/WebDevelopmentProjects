from selenium import webdriver
from selenium.webdriver.common.by import By

# Keep Chrome browser open after program finishes
chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)

driver = webdriver.Chrome(options=chrome_options)
driver.get("https://secure-retreat-92358.herokuapp.com/")

first_name_input = driver.find_element(By.NAME, value="fName")
first_name_input.send_keys("Bob")

last_name_input = driver.find_element(By.NAME, value="lName")
last_name_input.send_keys("Smith")

email_input = driver.find_element(By.NAME, value="email")
email_input.send_keys("BobSmith@gmail.com")

submit = driver.find_element(By.CSS_SELECTOR, "form button")
submit.click()

driver.quit()