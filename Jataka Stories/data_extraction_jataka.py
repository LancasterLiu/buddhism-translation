# 数据获取
# coding: utf-8
# author:liushuwen
# creation:2024-7-

import os
import time
from bs4 import *
from requests import *
from pandas import *

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
driver_path=r'D:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe'
options = Options()
options.headless = True
options.add_experimental_option("detach",True)
driver=webdriver.Chrome(driver_path,options=options)

chinese_texts = []
english_texts = []
i=1
# for i in [1,387]:
while i<548:
    link = f"https://jatakastories.div.ed.ac.uk/stories-in-text/jatakatthavannana-{i}"
    try:
        driver.get(link)
        # 英语
        translation_element = WebDriverWait(driver, 6).until(
            EC.presence_of_element_located((By.ID, "translation-text"))
        )
        translation_text = translation_element.text.strip()
        english_texts.append(translation_text)

        # 中文
        edition_element = WebDriverWait(driver, 6).until(
            EC.presence_of_element_located((By.ID, "edition-text"))
        )
        edition_text = edition_element.text.strip()
        chinese_texts.append(edition_text)
    except TimeoutException:
        print(f"Timeout occurred for link: {link}")
        pass
    except Exception as e:
        # print(f"An error occurred: {e}")
        pass
    i += 1
    # if i==1127:
    #     i=1231
    # elif i==1283:
    #     i=1317
    # else:
    #     i+=1


# 保存
df = DataFrame({'Pali': chinese_texts, 'english': english_texts})
csv_filename = os.path.join("Jataka Stories\Pali\Jātakatthavaṇṇanā.csv")
df.to_csv(csv_filename, index=False)
