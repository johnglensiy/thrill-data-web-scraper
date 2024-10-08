from importlib.metadata import Lookup

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common import StaleElementReferenceException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os

desktop_path = os.path.join(os.path.expanduser('~'), 'Desktop', 'wait_times_data')

options = FirefoxOptions()
options.set_preference('browser.download.folderList', 2)
options.set_preference('browser.download.dir', desktop_path)
options.set_preference("browser.download.manager.showWhenStarting", False)
options.set_preference("browser.download.manager.focusWhenStarting", False)
options.set_preference("browser.download.useDownloadDir", True)
options.set_preference("browser.helperApps.alwaysAsk.force", False)
options.set_preference("browser.download.manager.alertOnEXEOpen", False)
options.set_preference("browser.download.manager.closeWhenDone", True)
options.set_preference("browser.download.manager.showAlertOnComplete", False)
options.set_preference("browser.download.manager.useWindow", False)
# options.set_preference('browser.download.manager.showWhenStarting', False)
# options.set_preference('browser.download.manager.focusWhenStarting', False)

# options.add_argument('--headless')

driver = webdriver.Firefox(options=options)

login_URL = "https://www.thrill-data.com/users/login"
data_URL = "https://www.thrill-data.com/waits/attraction/disneyland/buzzlightyearastroblasters/"
login_data = {
    'username': 'johnsiyyy',
    'pass1': 'Roboticmaster27',
}
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) \
        AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Referer': 'https://www.thrill-data.com/users/login'
}


def login():
    print(f'Logging in...')
    driver.get(login_URL)

    username_field = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.XPATH, '//input[@name="username"]'))
    )

    password_field = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.XPATH, '//input[@name="pass1"]'))
    )

    login_button = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/form/input[4]'))
    )

    username_field.send_keys(login_data['username'])
    password_field.send_keys(login_data['pass1'])

    login_button.click()

    print("Successfully logged in!")

def get_cookies():
    cookies = {}
    selenium_cookies = driver.get_cookies()
    for cookie in selenium_cookies:
        cookies[cookie['name']] = cookie['value']
    return cookies

# def click_element():




def download_data():
    dl_categories = ["dl_jan", "dl_feb", "dl_mar",
              "dl_apr", "dl_may", "dl_jun", "dl_jul",
              "dl_aug", "dl_sep", "dl_oct", "dl_nov", "dl_dec"]
    print(f'Downloading data from {data_URL}...')
    driver.get(data_URL)
    for cat in dl_categories:
        dl_category = driver.find_element(By.ID, cat)
        print(dl_category.text)

        # error occurring here element is not clickable

        driver.execute_script("arguments[0].click();", dl_category)

        # include check for file existence
        wait = WebDriverWait(driver, 10, ignored_exceptions=[StaleElementReferenceException])
        dl_button = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Download Now!")))
        driver.execute_script("arguments[0].click();", dl_button)
        # dl_button.click()
        # dl_button = (WebDriverWait(driver, 10, ignored_exceptions=StaleElementReferenceException)
        #     EC.presence_of_element_located((By.LINK_TEXT, "Download Now!"))
        # ))

        # print(dl_button.text)
        # driver.execute_script("arguments[0].click();", dl_button)
        # dl_button.click()
        print(f'Data downloaded')

def main():
    login()
    get_cookies()
    download_data()
    driver.quit()

if __name__ == '__main__':
    main()


