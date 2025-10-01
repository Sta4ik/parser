from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import pandas as pd
import time
from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from random import randint

chrome_version = randint(110, 140)
windows_version = randint(10, 11)

opts = Options()
opts.add_argument(f"user-agent=Mozilla/5.0 (Windows NT {windows_version}.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{chrome_version}.0.0.0 Safari/537.36")
#opts.add_argument(f'--proxy-server=https://81.169.213.169:8888')

driver = webdriver.Chrome(options=opts)

driver.get('https://komp.1k.by/storage-usbflashdrives/')

def get_all_links_on_page():
    elements = driver.find_elements(By.CLASS_NAME, value='prod__link')
    listlinks = []
    for element in elements:
        listlinks.append(element.get_attribute('href'))

    return listlinks

page = driver.find_element(By.XPATH, value='/html/body/div[1]/main/div[3]/div[1]/div[53]/nav/a[6]').get_attribute('textContent')
page = int(page)
links = []
for item in range(1, page):
    driver.get(f'https://komp.1k.by/storage-usbflashdrives/page{item}')
    links.append(get_all_links_on_page())

finalLinks = []
for element in range(1, len(links)):
    for item in range(1, len(links[element])):
        finalLinks.append(links[element][item])

df = pd.DataFrame(columns=["Type", "Capacity", "Speed", "URL"])

for element in range(1, len(finalLinks)):
    driver.get(finalLinks[element])
    flash = []
    if(driver.find_element(By.XPATH, '//*[@id="product-data"]/div[1]/section/div[1]/div[1]/div/table/tbody/tr[1]/th/span').get_attribute('textContent') == 'Интерфейс'):
        flash.append(driver.find_element(By.XPATH, '//*[@id="product-data"]/div[1]/section/div[1]/div[1]/div/table/tbody/tr[1]/td').get_attribute('textContent'))
    else: 
        flash.append(None)
    if(driver.find_element(By.XPATH, '//*[@id="product-data"]/div[1]/section/div[1]/div/div/table/tbody/tr[2]/th/span').get_attribute('textContent') == 'Объем памяти'):
        flash.append(driver.find_element(By.XPATH, '//*[@id="product-data"]/div[1]/section/div[1]/div/div/table/tbody/tr[2]/td').get_attribute('textContent'))
    else:
        flash.append(None)
    if(driver.find_element(By.XPATH, '//*[@id="product-data"]/div[1]/section/div[1]/div/div/table/tbody/tr[3]/th/span').get_attribute('textContent') == 'Скорость чтения данных'):
        flash.append(driver.find_element(By.XPATH, '//*[@id="product-data"]/div[1]/section/div[1]/div/div/table/tbody/tr[3]/td').get_attribute('textContent'))
    else:
        flash.append(None)
    flash.append(finalLinks[element])
    df.loc[len(df)] = flash
df.to_csv('output2.csv', index=False, encoding='utf-8')
