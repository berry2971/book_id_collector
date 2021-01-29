import time
import random
import os
import getpass
from tqdm import tqdm
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import *
from bs4 import BeautifulSoup as bs4

MAX_SLEEP_SEC = 3
KEY_WORDS = []
ABS_PATH = os.path.dirname(os.path.abspath(__file__))
URL_MAIN = 'https://www.aladin.co.kr/home/welcome.aspx'
DRIVER = None

def getKeywords():
    lst = []
    with open(ABS_PATH + r'\keywords.txt', 'r', encoding='utf8') as f:
        lst.extend(f.readlines())
    return lst

def getUrl(keyword, page):
    return 'https://www.aladin.co.kr/search/wsearchresult.aspx?SearchTarget=All&SearchWord={keyword}&page={page}'.format(keyword=keyword, page=page)

### logic
print("\nBook ID Collector in Aladin\n")
KEY_WORDS = getKeywords()
DRIVER = webdriver.Chrome(ABS_PATH + r'\chromedriver.exe')

for keyword in tqdm(KEY_WORDS):
    bookIds = []
    page = 0
    while True:
        page += 1
        DRIVER.get(getUrl(keyword, page))

        try:
            divSearchResult = WebDriverWait(DRIVER, 5).until(EC.element_to_be_clickable((By.ID, "Search3_Result")))
            divBookDetails = divSearchResult.find_elements_by_class_name("ss_book_box")
            for divBookDetail in divBookDetails:
                bookId = divBookDetail.get_attribute("itemid")
                bookIds.append(bookId)
        except:
            with open(ABS_PATH + r'\res.txt', 'a', encoding='utf8') as f:
                f.write(keyword)
                f.write('\n')
                for bookId in bookIds:
                    f.write(bookId)
                    f.write('\n')
            break
