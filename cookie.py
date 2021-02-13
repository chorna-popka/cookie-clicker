from selenium import webdriver
import datetime as dt
from selenium.common.exceptions import StaleElementReferenceException

ROUND = 300
productivity = {
    "Cursor": 0.1,
    "Grandma": 1,
    "Farm": 8,
    "Mine": 47,
    "Factory": 260,
    "Bank": 1428,
    "Temple": 7926,
}

ch_drv_path = "/Users/svetulka/PycharmProjects/chromedriver"
URL = "https://orteil.dashnet.org/cookieclicker/"

driver = webdriver.Chrome(ch_drv_path)
driver.get(URL)

cookie = driver.find_element_by_id("bigCookie")
counter = driver.find_element_by_id("cookies")

start = int(dt.datetime.now().timestamp())
five_sec = int(dt.datetime.now().timestamp())


def five_sec_timer():
    return int(dt.datetime.now().timestamp()) - five_sec


def game_timer():
    return int(dt.datetime.now().timestamp()) - start


def check_stats():
    count = int(counter.text.split(" ")[0].replace(",", ""))
    return count


def buy_stuff():
    products = driver.find_elements_by_css_selector("div.product.unlocked")
    # get current roi of each unlocked product
    best_p = None
    best_roi = 9999999
    for p in products[:3]:
        price = int(p.find_element_by_class_name("price").text.split(" ")[0].replace(",", ""))
        try:
            roi = price / productivity[p.find_element_by_class_name("title").text]
        except KeyError:
            roi = 0  # if key not found - set roi to 0

        if roi < best_roi:
            best_roi = roi
            best_p = p
    # buy only the best
    while check_stats() > int(best_p.find_element_by_class_name("price").text.split(" ")[0].replace(",", "")):
        driver.execute_script("arguments[0].click();", best_p)


def buy_upgrades():
    try:
        upgrades = driver.find_elements_by_css_selector("div.crate.upgrade.enabled")
    except StaleElementReferenceException:
        upgrades = driver.find_elements_by_css_selector("div.crate.upgrade.enabled")

    if len(upgrades) > 0:
        driver.execute_script("arguments[0].click();", upgrades[0])
        buy_upgrades()


while True:
    cookie.click()
    if five_sec_timer() >= 3:
        five_sec = int(dt.datetime.now().timestamp())
        buy_upgrades()
        buy_stuff()

    if game_timer() >= ROUND:
        break

print(counter.find_element_by_tag_name("div").text)
driver.quit()
