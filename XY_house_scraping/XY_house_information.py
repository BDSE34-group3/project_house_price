""" 基本套件 """
import requests as req
from bs4 import BeautifulSoup as bs
from time import sleep
from pprint import pprint
import pandas as pd
import logging as log
import json

# 處理正則表達式
import re 

# 執行 系統命令(commend)
import os

# 讓執行中可能會跑出的warnings閉嘴
import warnings
warnings.filterwarnings("ignore") 

import httpx
import ssl

""" selenium套件 """
# 瀏覽器自動化
from selenium import webdriver as wd
from selenium.webdriver.chrome.service import Service

# (三人行) 在動態網頁中，等待指定元素出現的工具(要等多久?)
from selenium.webdriver.support.ui import WebDriverWait
# (三人行) 當指定元素出現，便符合等待條件 → 停止等待階段，並往下一段程式碼執行
from selenium.webdriver.support import expected_conditions as EC
# (三人行) 以...搜尋指定物件 (如: ID、Name、連結內容等...)
from selenium.webdriver.common.by import By 

# 處理逾時例外的工具 (網頁反應遲緩 or 網路不穩定)
from selenium.common.exceptions import TimeoutException

# 加入行為鍊 ActionChain (在 WebDriver 中模擬滑鼠移動、點擊、拖曳、按右鍵出現選單，以及鍵盤輸入文字、按下鍵盤上的按鈕等)
from selenium.webdriver.common.action_chains import ActionChains

# 加入鍵盤功能 (例如 Ctrl、Alt 等)
from selenium.webdriver.common.keys import Keys


""" 設定log檔 """
def set_log():
    # 基本設定
    logger = log.getLogger('XY_house.log')

    # 設定等級
    logger.setLevel(log.INFO)

    # 設定輸出格式
    formatter = log.Formatter('%(asctime)s - %(levelname)s - %(message)s', "%Y-%m-%d %H:%M:%S")

    # 儲存在 log 當中的事件處理器
    fileHandler = log.FileHandler('XY_house_NewTaipei.log', mode='a', encoding='utf-8') # a: append, w: write
    fileHandler.setFormatter(formatter)

    # 輸出在終端機介面上的事件處理器
    console_handler = log.StreamHandler()
    console_handler.setFormatter(formatter)

    # 加入事件
    logger.addHandler(console_handler)
    logger.addHandler(fileHandler)

    return logger

""" 從先前爬取的檔案中，讀取裡面的網址 """
def get_house_list(path: str):
    with open('C:\\python_web_scraping\\XY_house_scraping\\XY_house_Taipei\\XY_house_urls_Taipei.json', encoding='utf-8') as f:
        data = f.read()
    house_list = json.loads(data)
    return house_list

""" 用迴圈開啟信義房屋的網址，並爬取資料 """
def XY_url(partial_url):
    url = f"https://www.sinyi.com.tw{partial_url}"

    # headers = {
    #     "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"
    # }

    # # 發送 GET 請求到 URL (verify=False)
    # response = req.get(url, headers=headers)

    # 創建一個 SSL 上下文對象
    ssl_context = ssl.create_default_context()
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE

    # 使用 httpx 和自定義的 SSL 上下文發送 GET 請求
    try:
        with httpx.Client(verify=ssl_context) as client:
            response = client.get(url)
            
    except httpx.RequestError as e:
        print(f"Request failed: {e}")
        return None
    
    print(response.status_code)

    # 檢查請求是否成功
    if response.status_code == 200:
        # 解析網頁的 HTML 內容
        soup = bs(response.text, 'html.parser')
        # 創建一個字典來儲存數據
        data = []
        
        # 區塊一
        try:
            block1 = soup.find('div', class_='buy-content-title-name')
            data['物件名稱'] = block1.find('div', class_='buy-content-title-name').text.strip()
        except Exception as e:
            logger.error(f"url:{url} 區塊一出現錯誤: {e}")
            return None
        

        # 區塊二
        try:
            block2 = soup.find('div', class_='buy-content-detail-bar')

            block2_1 = block2.find('div', class_='buy-content-detail-area')
            span = block2_1

            data[f'{span[0]}'] = span[1]
            data[f'{span[2]}'] = span[3]

            data['室內格局'] = block2.find('div', class_='buy-content-detail-layout').text.strip()
            data['物件狀態'] = block2.find('div', class_='buy-content-detail-type').text.strip()
            data['樓層資訊'] = block2.find('div', class_='buy-content-detail-floor').text.strip()

        except Exception as e:
            logger.error(f"url:{url} 區塊二出現錯誤: {e}")
            return None
        

        # 區塊三
        try:
            block3 = soup.find_all('div', class_='buy-content-basic-cell')
            tital = block3
            value = block3

            for b3 in block3:
                data[f'{tital}'] = b3.find('div', class_='basic-title').get_text(strip=True)
                data[f'{value}'] = b3.find('div', class_='basic-value').get_text(strip=True)

        except Exception as e:
            logger.error(f"url:{url} 區塊三出現錯誤: {e}")
            return None 
            
            
        return data

    else:
        print(f"數據擷取失敗: {response.status_code}")
        return {}

# 於爬蟲結束後顯示最終結果 
def test():
    total_house_info = []
    error_house_list = []

if __name__ == "__main__":
    
    logger = set_log()

    # 初始化存儲抓取失敗 URL 的列表
    error_house_list = []

    # 讀取房屋list檔案
    house_list_path = 'C:\\python_web_scraping\\XY_house_scraping\\XY_house_Taipei\\XY_house_urls_Taipei.json'
    readurl = get_house_list(house_list_path)

    for url in readurl:
        house_data = XY_url(url)
        if house_data:
            logger.info(f"已成功抓取房屋資料：{house_data}")
        else:
            logger.error(f"無法抓取房屋資料，URL：{url}")
            error_house_list.append(url)

    # openurl = XY_url()
    
    logger.info('XY_房屋資料抓取完畢')
    if error_house_list:
        logger.info(f"以下 URL 抓取失敗：{error_house_list}")

    h_list = XY_url('house_urls_NewTaipei.json')

    
    

# 範例使用：
# result = xy_url('/buy/house/67080J/?breadcrumb=list')
# print(result)