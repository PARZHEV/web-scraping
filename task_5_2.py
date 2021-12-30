#!/usr/bin/env python
# coding: utf-8

# In[ ]:


2) Написать программу, которая собирает товары «В тренде» с сайта техники mvideo и складывает данные в БД. 
Сайт можно выбрать и свой. Главный критерий выбора: динамически загружаемые товары


# In[1]:


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common import exceptions
from lxml import html
from selenium.webdriver.common.action_chains import ActionChains
import time
from pymongo import MongoClient
from pprint import pprint
import pymongo


# In[31]:


chrome_options = Options()
chrome_options.add_argument('start-maximized')
# chrome_options.add_argument('--window-size=1920,1080')

driver = webdriver.Chrome(options=chrome_options)
# driver.implicitly_wait(10)

driver.get('https://www.mvideo.ru/')

body = driver.find_element_by_css_selector('body')
body.send_keys(Keys.PAGE_DOWN)

results = []
pages = 0
while True:
    try:
        
        driver.implicitly_wait(5)           
        button = driver.find_element(By.XPATH, "//mvid-simple-product-collection/mvid-carousel/div/button[contains(@class, 'btn forward')]")   
        button.click()        
    except:
        print('Finish')
        break
goods = driver.find_elements(By.XPATH, "//mvid-simple-product-collection-mp[1]/mvid-simple-product-collection//mvid-carousel/div/div/mvid-product-cards-group/div/div/a/div")
for good in goods:
    names = {}
    name = good.find_element(By.XPATH, "//div/a[@class='ng-star-inserted']").text
    names['name'] = name
    results.append(names)


# In[32]:


print(results)


# In[ ]:


client = MongoClient("mongodb+srv://<USER>:<Pass>@mylittlecluster.twgzn.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
db = client.newdata
mvideo_names = db.mvideo_names

for result in results:
    try:
        mvideo_names.insert_one(result)
    except:
        pass

