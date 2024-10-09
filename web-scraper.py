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
from selenium.common.exceptions import TimeoutException
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

def check_for_element(locator, max_retries=3):
    # access download link div
    for attempt in range(max_retries):
        try:
            # Wait for up to 10 seconds for the element to be present
            element = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located(locator)
            )
            print("element is present")
            return element
        except TimeoutException:
            print(f"Attempt {attempt + 1} failed - element is not present yet")
    return None

    # for attempt in range(max_retries):
    #     try:
    #         # Attempt download
    #         download_button = driver.find_element_by_css_selector('.download-csv')
    #         download_button.click()
    #
    #         # Wait for download to complete
    #         time.sleep(5)
    #         return True
    #     except Exception as e:
    #         print(f"Download attempt {attempt + 1} failed: {str(e)}")
    #         time.sleep(2)
    # return False

def download_data():
    dl_categories = ["dl_jan", "dl_feb", "dl_mar",
              "dl_apr", "dl_may", "dl_jun", "dl_jul",
              "dl_aug", "dl_sep", "dl_oct", "dl_nov", "dl_dec"]
    print(f'Downloading data from {data_URL}...')
    driver.get(data_URL)
    for cat in dl_categories:
        # check for download-link div which is container for dynamically loaded button
        download_div = check_for_element((By.ID, "download-link"))

        # find category button and click it (seems to consistently work)
        dl_category = driver.find_element(By.ID, cat)
        print(dl_category.text)
        driver.execute_script("arguments[0].click();", dl_category)

        # check if download link was made available
        children = download_div.find_elements()
        for child in children:
            print(child.text)
        # include check for file existence

        # check for download-button
        check_for_element((By.LINK_TEXT, "Download Now!"))
        wait = WebDriverWait(driver, 30, ignored_exceptions=[StaleElementReferenceException])

        # don't wait for element to be clickable find it instead
        dl_button = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Download Now!")))
        driver.execute_script("arguments[0].click();", dl_button)

        # timeout exception for whatever reason
        # download button is contained inside a download div
        # whenever a category button is clicked it dynamically loads the button inside said div
        # workflow
        #   check for existence of download div and print it
        #   check for existence of download button and print it


        print(f'Data downloaded')
        print(f'----------------------------------------------------------------')

def main():
    login()
    get_cookies()
    download_data()
    driver.quit()

if __name__ == '__main__':
    main()


