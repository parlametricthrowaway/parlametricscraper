from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementNotInteractableException
from datetime import date
import os
import csv
import pandas as pd
import streamlit as st
from datetime import datetime


def save_to_csv(url_list, name_list, org_number, phone_number, email, latitudes, longitudes, coordinates_url):

    df = {
            'Url': url_list,
            'Name': name_list,
            'org_number': org_number,
            'phone_number': phone_number,
            'email': email,
            'latitudes': latitudes,
            'longitudes': longitudes,
            'coordinates_urls': coordinates_url
    }

    df = pd.DataFrame(df)
    now = datetime.now()
    current_date = now.strftime("%Y-%m-%d")
    dir_path = os.getcwd() + "/" + "csv_files"
    if not os.path.exists(dir_path):
        os.makedirs(directory_name)
    df.to_csv(dir_path + "/" + f'{current_date}.csv', index=False)


def get_driver():
    options = Options()
    options.add_extension(os.getcwd() + "\cookieblocker.crx")
    options.headless = False
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
    driver.implicitly_wait(10)
    return driver


def get_org_number(selected_org_number):
    selected_org_number = selected_org_number.replace("Org nr<!-- -->: <!-- -->", '')
    selected_org_number = selected_org_number.replace("org", '')
    selected_org_number = selected_org_number.replace("MGD Sport", '')
    selected_org_number = selected_org_number.replace("-", '')
    if selected_org_number == '':
        selected_org_number = "no info"
    return selected_org_number


def get_phone_number(selected_phone_number):
    selected_phone_number = selected_phone_number.replace(' ', '')
    selected_phone_number = selected_phone_number.replace('-', '')
    selected_phone_number = selected_phone_number.replace('Tele<!>:<!>', '')
    selected_phone_number = selected_phone_number.replace('+', '')
    return selected_phone_number


def get_coordinates(selected_coordinates):
    selected_coordinates = selected_coordinates.replace('http://www.google.com/maps/place/', "")
    selected_coordinates = selected_coordinates.replace(",", " ")
    latitude = selected_coordinates.split()[0]
    longitude = selected_coordinates.split()[1]
    return latitude, longitude


def xpath_test(url_list, driver):
    name_list = []
    org_number = []
    phone_number = []
    email = []
    coordinates_url = []
    latitudes = []
    longitudes = []
    for url in url_list:
        driver.get(url)
        try:
            name_list.append(driver.find_element(By.XPATH, '//*[@id="__next"]/div/main/section[5]/p/span[1]').get_attribute("innerHTML"))
            selected_org_number = driver.find_element(By.XPATH, '//*[@id="__next"]/div/main/section[5]/p/span[2]').get_attribute("innerHTML")
            selected_org_number = get_org_number(selected_org_number)
            org_number.append(selected_org_number)
            selected_phone_number = driver.find_element(By.XPATH, '//*[@id="__next"]/div/main/section[5]/p/span[3]').get_attribute("innerHTML")
            selected_phone_number = get_phone_number(selected_phone_number)
            phone_number.append(selected_phone_number)
            email.append(driver.find_element(By.XPATH, '//*[@id="__next"]/div/main/section[5]/p/span[4]').get_attribute("innerHTML"))
            selected_coordinates = driver.find_element(By.XPATH, '//*[@id="__next"]/div/main/section[2]/a').get_attribute('href')
            coordinates_url.append(selected_coordinates)
            latitude, longitude = get_coordinates(selected_coordinates)
            latitudes.append(latitude)
            longitudes.append(longitude)
        except NoSuchElementException:
            name_list.append(driver.find_element(By.XPATH, '//*[@id="__next"]/div/main/section[5]/section[2]/p/span[1]').get_attribute("innerHTML"))
            selected_org_number = driver.find_element(By.XPATH, '//*[@id="__next"]/div/main/section[4]/p/span[2]').get_attribute("innerHTML")
            selected_org_number = get_org_number(selected_org_number)
            org_number.append(selected_org_number)
            selected_phone_number = driver.find_element(By.XPATH, '//*[@id="__next"]/div/main/section[4]/p/span[3]').get_attribute("innerHTML")[-11:]
            selected_phone_number = get_phone_number(selected_phone_number)
            phone_number.append(selected_phone_number)
            email.append(driver.find_element(By.XPATH, '//*[@id="__next"]/div/main/section[4]/p/span[4]').get_attribute("innerHTML"))
            selected_coordinates = driver.find_element(By.XPATH, '//*[@id="__next"]/div/main/section[2]/a').get_attribute('href')
            coordinates_url.append(selected_coordinates)
            latitude, longitude = get_coordinates(selected_coordinates)
            latitudes.append(latitude)
            longitudes.append(longitude)
    return name_list, org_number, phone_number, email, latitudes, longitudes, coordinates_url


def list_iterator(start, finish, driver):
    url_list = []
    for selected_number in range(start, finish+1):
        url_list.append(driver.find_element(By.XPATH, f'//*[@id="__next"]/div/main/section[1]/section[2]/article[{selected_number}]/section[2]/div[2]/a').get_attribute('href'))
    name_list, org_number, phone_number, email, latitudes, longitudes, coordinates_url = xpath_test(url_list, driver)
    save_to_csv(url_list, name_list, org_number, phone_number, email, latitudes, longitudes, coordinates_url)


def main_scraper():
    driver = get_driver()
    website_url = "https://www.kayakomat.com/sv/locations"
    driver.get(website_url)
    list_iterator(1, 80, driver)




