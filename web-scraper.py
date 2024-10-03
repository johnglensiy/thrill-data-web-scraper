from importlib.metadata import Lookup

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

options = Options()
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

def download_data():
    print(f'Downloading data from {data_URL}...')
    driver.get(data_URL)
    dl_category = driver.find_element(By.ID, 'dl_day')

    dl_category.click()
    dl_button = driver.find_element(By.XPATH, '/html/body/div[2]/div[13]/div[2]/div[31]/div/div[3]/a')
    dl_button.click()
    print(f'Data downloaded')


def main():
    login()
    get_cookies()
    download_data()
    driver.quit()

if __name__ == '__main__':
    main()


