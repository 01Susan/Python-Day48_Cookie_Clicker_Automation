# import required libraries
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time

# website URL to automate clicking on cookie
cookie_website = "http://orteil.dashnet.org/experiments/cookie/"

# path to the Chrome driver executable file
chrome_drive_path = r"D:\Downloads\chromedriver_win32\chromedriver.exe"

# initialize Chrome driver service
chrome_service = Service(chrome_drive_path)

# create a new Chrome driver instance
driver = webdriver.Chrome(service=chrome_service)

# open the cookie website using the driver
driver.get(cookie_website)

# locate the cookie element on the webpage
cookie = driver.find_element(by=By.ID, value="cookie")

# get the ID of all the upgrade items available on the webpage
items = driver.find_elements(by=By.CSS_SELECTOR, value="#store div")
item_id = [item.get_attribute("id") for item in items]

# set the timeout for checking the upgrades to be enabled as 5 seconds
time_out = time.time() + 5

# set the total game time to be 5 minutes
five_min = time.time() + 300

# start the game loop
while True:
    # click the cookie element
    cookie.click()

    # check if it's time to check for upgrades
    if time.time() > time_out:
        # get the prices of all the upgrades available
        all_prices = driver.find_elements(by=By.CSS_SELECTOR, value="#store b")
        item_price = []

        # extract the price of each upgrade as an integer
        for price in all_prices:
            price_text = price.get_attribute("textContent")
            if price_text != "":
                price_int = int(price_text.split("-")[-1].strip().replace(",", ""))
                item_price.append(price_int)

        # create a dictionary of the available upgrades and their prices
        cookie_upgrades = {ids: price for ids, price in zip(item_id, item_price)}

        # get the amount of cookies the player has
        cookie_money = int(driver.find_element(by=By.ID, value="money").text.replace(",", "").strip())

        # find the upgrades that can be afforded
        affordable_upgrades = {}
        for ids, price in cookie_upgrades.items():
            if cookie_money > price:
                affordable_upgrades[ids] = price

        # purchase the most expensive upgrade that can be afforded
        highest_price_upgrade = max(affordable_upgrades.values())
        highest_ids = ""
        for ids, price in affordable_upgrades.items():
            if price == highest_price_upgrade:
                highest_ids = ids
        driver.find_element(by=By.ID, value=highest_ids).click()

        # set the timeout for the next upgrade check to 10 seconds from now
        time_out = time.time() + 10

    # check if it's time to end the game
    if time.time() > five_min:
        # display the cookies per second (cps) value
        cookie_per_sec = driver.find_element(by=By.ID, value="cps")
        print(cookie_per_sec.text)

        # break out of the game loop
        break
