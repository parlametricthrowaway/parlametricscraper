import selenium
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import os
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
import time
from selectorlib import Extractor
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.support.ui import WebDriverWait
import streamlit as st
import re
import scraper.extractor as extract
import webdesign.design as design

def show_text(txt_file_name):
    desktop_dir = os.path.join(os.path.expanduser('~'), 'Desktop')
    txt_file_dir = desktop_dir + f"/my_folder/{txt_file_name}.txt"
    st.write(txt_file_dir)
    st.write("here it is the txt file name")
    extract.main(txt_file_dir)




def get_facebook_page_name(facebook_url):
    input_string = facebook_url.split("facebook.com/")[1]
    if "/" in input_string:
        input_string = input_string.split('/')[0]

    return input_string


def create_folder(unfiltered_comments, facebook_page_name):
    desktop_path = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
    folder_path = os.path.join(desktop_path, 'my_folder')

    if not os.path.exists(folder_path):
        os.mkdir(folder_path)

    file_path = os.path.join(folder_path, f'{facebook_page_name}.txt')

    if os.path.exists(file_path):
        with open(file_path, "a+", encoding='utf-8') as file:
            file.write(unfiltered_comments)
    else:
        with open(file_path, "a+", encoding='utf-8') as file:
            file.write(unfiltered_comments)


def remove_crap(unfiltered_comments):
    filtered_comments = []
    comment = remove_crap_from_list(unfiltered_comments)
    filtered_comments.append(comment)
    return filtered_comments


def get_comments():
    driver = get_driver()
    divs = driver.find_elements(By.TAG_NAME, 'div')
    for div in divs:
        st.write(div.text)
    time.sleep(20)


def get_driver():
    options = Options()
    options.add_extension(os.getcwd() + "\cookieblocker.crx")
    options.headless = False
    options.add_argument("--disable-infobars")
    options.add_argument("start-maximized")
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
    driver.implicitly_wait(4)
    return driver


def main_scraper(website_url):
    driver = get_driver()
    driver.get(website_url)
    time.sleep(3)
    spans = driver.find_elements(By.TAG_NAME, 'span')
    #for element in spans:
        #try:
            #if element.text == "Visa 5 kommentarer till":
                #driver.execute_script("arguments[0].click();", element)
                #break
        #except StaleElementReferenceException:
            #pass
    div_list = []
    divs = driver.find_elements(By.TAG_NAME, 'div')
    for div in divs:
        try:
            div_list.append(div.text)
        except StaleElementReferenceException:
            pass

    facebook_page_name = get_facebook_page_name(website_url)
    unfiltered_comments = list(set(div_list))
    unfiltered_comments = ' '.join(unfiltered_comments)
    create_folder(unfiltered_comments, facebook_page_name)
    show_text(facebook_page_name)
    time.sleep(35)
    