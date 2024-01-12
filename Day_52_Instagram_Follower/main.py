from selenium import webdriver
from selenium.common import NoSuchElementException, ElementClickInterceptedException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from config import USERNAME, PASSWORD, SIMILAR_ACCOUNT
import time

FOLLOWER_COUNT_LIMIT = 10


class InstaFollower:

    def __init__(self):
        # Keep Chrome browser open after program finishes
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_experimental_option("detach", True)

        self.driver = webdriver.Chrome(options=chrome_options)

    def login(self):
        self.driver.get("https://www.instagram.com")
        time.sleep(10)

        try:
            cookie_warning = self.driver.find_element(By.XPATH,
                                                      "/html/body/div[4]/div[1]/div/div[2]/div/div/div/div/div[2]/div/button[2]")
            if cookie_warning:
                cookie_warning.click()
        except NoSuchElementException:
            pass

        time.sleep(5)

        username = self.driver.find_element(By.NAME, value="username")
        password = self.driver.find_element(By.NAME, value="password")
        username.send_keys(USERNAME)
        password.send_keys(PASSWORD)

        time.sleep(2)

        password.send_keys(Keys.ENTER)

        time.sleep(5)

    def find_followers(self):
        time.sleep(5)
        self.driver.get(f"https://www.instagram.com/{SIMILAR_ACCOUNT}")

        time.sleep(50)

        follower_list = self.driver.find_element(By.PARTIAL_LINK_TEXT, "followers")
        follower_list.click()

    def follow(self):
        time.sleep(50)
        follow_buttons = self.driver.find_elements(By.CSS_SELECTOR, "._aano button")

        time.sleep(5)

        print(follow_buttons)

        for i in range(FOLLOWER_COUNT_LIMIT):
            try:
                follow_button = follow_buttons[i]
                follow_button.click()
                time.sleep(1)
            except ElementClickInterceptedException:
                try:
                    cancel_button = self.driver.find_element(By.XPATH, "//button[contains(text(), 'Cancel')]")
                    if cancel_button:
                        cancel_button.click()
                        time.sleep(1)
                except NoSuchElementException:
                    pass


insta_follower = InstaFollower()
insta_follower.login()
insta_follower.find_followers()
insta_follower.follow()
