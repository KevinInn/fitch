from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import pandas as pd
driver = webdriver.Chrome()
driver.get("https://www.fitchratings.com/entity/tanzania-88305871#ratings")

time.sleep(10)

#抓取tabs用來進行翻頁
containerClass = 'react-tabs__tab-list'  
tabsConatiner = driver.find_element(By.CLASS_NAME, containerClass)
tabs = tabsConatiner.find_elements(By.TAG_NAME, 'li')

dates = []
ratings = []
ratingKeys = []
actions = []
#透過click每個tab，抓取內部資料
for tab in tabs:
    #click翻頁
    tab.click()
    #抓取整個Rating Container
    ratingContainer = driver.find_element(By.CLASS_NAME, "react-tabs")
    #抓取Rating Container的HTML內容
    ratingContent = ratingContainer.get_attribute('innerHTML')
    ratingHtml = BeautifulSoup(ratingContent, 'html.parser')
    # 開始使用Bs4讀取內部資料
    panel = ratingHtml.find('div', class_='react-tabs__tab-panel react-tabs__tab-panel--selected')
    dataTable = panel.find('table').find('tbody')
    trs = dataTable.find_all('tr')
    for tr in trs:
        print(tr)
    #將Lists轉換為dataframes
    data = {
        'Dates': dates,
        'Ratings': ratings,
        'RatingKeys': ratingKeys,
        'Actions': actions
    }
    df = pd.DataFrame(data)
driver.close()
