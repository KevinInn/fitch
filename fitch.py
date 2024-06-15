from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import pandas as pd

def getTrType(td: str):
    if "date" in td.text.lower():
        return "dates"
    elif "rating" in td.text.lower():
        return "ratings"
    elif "action" in td.text.lower():
        return "actions"

driver = webdriver.Chrome()
driver.get("https://www.fitchratings.com/entity/tanzania-88305871#ratings")

time.sleep(10)

#抓取heading
headerConatinerClass = 'article__header'
header = driver.find_element(By.CLASS_NAME, headerConatinerClass)
headerClass = 'heading--1'
header = header.find_element(By.CLASS_NAME, headerClass)
countryName = header.text

#抓取tabs用來進行翻頁
containerClass = 'react-tabs__tab-list'  
tabsConatiner = driver.find_element(By.CLASS_NAME, containerClass)
tabs = tabsConatiner.find_elements(By.TAG_NAME, 'li')

ratingTypeList = []
dates = []
ratings = []
# ratingKeys = []
actions = []
df = pd.DataFrame()
#透過click每個tab，抓取內部資料
for tab in tabs:
    #click翻頁
    ratingType = tab.text
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
        tds = tr.find_all('td')
        trType = ""
        for index, td in enumerate(tds):
            if index == 0:
                trType = getTrType(td)
                continue
            ratingTypeList.append(ratingType)
            if trType == "dates":
                dates.append(td.text)
            elif trType == "ratings":
                ratings.append(td.text)
            elif trType == "actions":
                actions.append(td.text)
    # 將Lists轉換為dataframes
data = {
    'Rating Type': ratingTypeList,
    'Dates': dates,
    'Ratings': ratings,
    # 'RatingKeys': ratingKeys,
    'Actions': actions
}
df = pd.DataFrame(data)
df.insert(0, 'Country Name', countryName)


csv_filename = 'afat.csv'
df.to_csv(csv_filename, mode='a', header=False, index=False)

driver.close()

