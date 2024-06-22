# 数据获取
# coding: utf-8
# author:liushuwen
# creation:2024-5-5

import os
from bs4 import *
from requests import *
from pandas import *

org_link="https://ctext.org/"
part = "rulin-waishi/"
subpart=""
headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36 Edg/98.0.1108.62"}
link=org_link+part+subpart
r=get(link,headers=headers)

soup=BeautifulSoup(r.text,"html.parser")
header=soup.find('h2').text.strip()
# Create a folder
if not os.path.exists(header):
    os.makedirs(header)
# if not os.path.exists(part):
#     os.makedirs(part)
# if not os.path.exists(part+header):
#     os.makedirs(part+header)
    
# 找到文本元素
texts=soup.find('div',id="content2")
# Find all sublinks
sublinks = texts.find_all('a', href=True)
# try_=sublinks[17]['href']
# print(try_.startswith(part))

for j in range(17,19):
    sublink=sublinks[j]
    href = sublink['href']
    if href.startswith(part) and '#' not in href:
        sublink_url = org_link + href
        sublink_name = sublink.text.strip()
        
        # Create a folder for each sublink
        # sublink_folder = os.path.join(folder, sublink_name)
        # if not os.path.exists(sublink_folder):
        #     os.makedirs(sublink_folder)
        
        # Fetch content from each sublink
        r_sublink = get(sublink_url, headers=headers)
        soup_sublink = BeautifulSoup(r_sublink.text, "html.parser")
        alltext = soup_sublink.find('div', id="content3")
        ctext = alltext.find_all('td', class_=lambda x: x and "ctext" in x.split() and "opt" not in x.split())
        etext = alltext.find_all('td', class_=lambda x: x and "etext" in x.split() and "opt" not in x.split())
        if len(ctext)!=len(etext):
            print("check:",sublink_url)
            continue
        chinese_texts = []
        english_texts = []
        
        for i in range(1, len(ctext), 2):
            chinese_text = ctext[i].text.strip()
            chinese_texts.append(chinese_text)
        
        for i in range(1, len(etext), 2):
            english_text = etext[i].text.strip()
            english_texts.append(english_text)
        
        # if j==37:
        #     chinese_texts.insert(4, english_texts[4])
        #     english_texts.pop(4)
        # Write content to a CSV file within sublink folder
        df = DataFrame({'chinese': chinese_texts, 'english': english_texts})
        sublink_name=sublink_name.replace('"', '').replace(':', '_')
        csv_filename = os.path.join(header, sublink_name + ".csv")
        df.to_csv(csv_filename, index=False)
