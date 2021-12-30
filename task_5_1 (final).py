#!/usr/bin/env python
# coding: utf-8

# In[5]:


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
from pymongo import MongoClient
from pprint import pprint
from pymongo.errors import DuplicateKeyError as dke
import hashlib


# In[7]:


driver = webdriver.Chrome()

driver.get('https://account.mail.ru/login')

driver.implicitly_wait(5)

elem = driver.find_element(By.NAME, "username")
elem.send_keys('study.ai_172@mail.ru')

elem.send_keys(Keys.ENTER)

elem = driver.find_element(By.NAME, "password")
elem.send_keys('NextPassword172#')

elem.send_keys(Keys.ENTER)

results = []

for i in range(5):
    
    articles = driver.find_elements(By.XPATH, "//div/a[contains(@class,'llc js-tooltip-direction_let')]")
    actions = ActionChains(driver)
    actions.move_to_element(articles[-1])
    actions.perform()
    
    mails = driver.find_elements(By.XPATH, "//div/a[contains(@class,'llc js-tooltip-direction_let')]")
    
    

    for mail in mails:
        letters = {}

        _id = mail.get_attribute('data-uidl-id')
        from_whom = mail.find_element(By.XPATH, ".//div/span[@class='ll-crpt']").text
        date = mail.find_element(By.XPATH, ".//div/div[@class='llc__item llc__item_date']").text
        mail_topic = mail.find_element(By.XPATH, ".//span/span[@class='ll-sj__normal']").text
        full_text = mail.find_element(By.XPATH, ".//span/span[@class='ll-sp__normal']").text

        letters['_id'] = _id
        letters['from_whom'] = from_whom
        letters['date'] = date
        letters['mail_topic'] = mail_topic
        letters['full_text'] = full_text

        results.append(letters)

        
    
    


# In[13]:


client = MongoClient("mongodb+srv://<USER>:<Pass>@mylittlecluster.twgzn.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
db = client.newdata
mails = db.mails

for result in results:
    try:
        mails.insert_one(result)
    except:
        pass
        

