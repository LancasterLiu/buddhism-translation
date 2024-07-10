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
from selenium.webdriver.support import expected_conditions as EC
driver_path=r'D:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe'
options = Options()
options.headless = True
options.add_experimental_option("detach",True)
driver=webdriver.Chrome(driver_path,options=options)

chinese_texts = []
english_texts = []
i=1
while i<41:
    link="https://jatakastories.div.ed.ac.uk/stories-in-text/avadanasataka-%d"%i
    # headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"}
    # r=get(link,headers=headers)
    # 找到文本元素
    driver.get(link)
    # 英语
    translation_element = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.ID, "translation-text"))
    )
    translation_text = translation_element.text.strip()
    # translation_text = soup.find('div',id="translation-text")
    english_texts.append(translation_text)

    # 中文
    edition_element = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.ID, "edition-text"))
    )
    edition_text = edition_element.text.strip()
    chinese_texts.append(edition_text)
    # i+=1
    if i==20:
        i=22
    elif i==9:
        i=11
    else:
        i+=1


# soup=BeautifulSoup(r.text,"html.parser"
# # print(soup)
# print(english_texts)

# edition_text = soup.find('div', id='edition-text')

# print(edition_text)



# 保存
df = DataFrame({'Sanskrit': chinese_texts, 'english': english_texts})
csv_filename = os.path.join("Jataka Stories\sanskrit\Avadānaśataka.csv")
df.to_csv(csv_filename, index=False)
