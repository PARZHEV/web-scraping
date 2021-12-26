#!/usr/bin/env python
# coding: utf-8

# In[ ]:


1. Написать приложение, которое собирает основные новости с сайта на выбор news.mail.ru, lenta.ru, yandex-новости. 
Для парсинга использовать XPath. Структура данных должна содержать:
название источника;
наименование новости;
ссылку на новость;
дата публикации
2. Сложить собранные новости в БД


# In[4]:


from lxml import html
import requests
from pprint import pprint
import re
from pymongo import MongoClient

url = 'https://lenta.ru/'
header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36'}

response = requests.get(url, headers=header)

dom = html.fromstring(response.text)

items = dom.xpath("//div[@class='topnews__column']/a")

newsall = []
for item in items:
    news = {}
    source = 'https://lenta.ru/'
    news_name = item.xpath(".//div/span[@class='card-mini__title']/text()")[0]
    news_link = item.xpath(".//div/span[@class='card-mini__title']/../../@href")[0]
    if len(news_link) > 100:
        news_link
    else:
        news_link = f'https://lenta.ru/{news_link}'
    placment_date = re.findall(r'\d+.\d+.\d+', news_link)[0]

    news['source'] = source
    news['news_name'] = news_name
    news['news_link'] = news_link
    news['placment_date'] = placment_date
    
    newsall.append(news)
    
pprint(newsall)


# In[8]:


# Сложить собранные новости в БД (онлайн база)
client = MongoClient("mongodb+srv://<USER>:<Pass>littlecluster.twgzn.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
db = client.test


news = db.news

news.insert_many(newsall)


# In[ ]:




