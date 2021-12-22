#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# 1. Развернуть у себя на компьютере/виртуальной машине/хостинге MongoDB и реализовать функцию, 
# которая будет добавлять только новые вакансии/продукты в вашу базу.


# In[5]:


import pymongo
from pymongo import MongoClient
from pprint import pprint
from pymongo.errors import DuplicateKeyError as dke
import hashlib
from bs4 import BeautifulSoup as bs
import requests
from pprint import pprint
import re


# In[2]:


# https://hh.ru/search/vacancy?clusters=true&area=1&no_magic=true&ored_clusters=true&enable_snippets=true&salary=&text=Менеджер
main_url = 'https://hh.ru'


params = {'text': 'менеджер',
         'clusters':'true',
         'area':'1',
         'no_magic':'true',
          'ored_clusters':'true',
          'enable_snippets':'true',
          'salary':'',
          'page':1}

headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.85 YaBrowser/21.11.2.773 Yowser/2.5 Safari/537.36'}

response = requests.get(main_url+'/search/vacancy/',params=params, headers=headers)



dom = bs(response.text, 'html.parser')
name_vacancy = dom.find_all('div',{'class':'vacancy-serp-item'})

vacancy_list = []

for vacancy in name_vacancy:
    vacancy_data = {}
    info = vacancy.find('a',{'class','bloko-link'})
        # Наименование вакансии.
    name = info.text
        # Предлагаемую зарплату (разносим в три поля: минимальная и максимальная и валюта. цифры преобразуем к цифрам).
    pTag = vacancy.find('span',{'class', 'bloko-header-section-3'})
    b = pTag.find_next('span',{'class', 'bloko-header-section-3'}).text
    c = re.findall(r'\d+', b)

    try:
        min_salary = int(c[0]+c[1])
        max_salary = int(c[2]+c[3])
    except :
        min_salary = ''

    curency_salary = re.findall(r'\s\D\D\D', b)
    curency_salary = str(curency_salary[0])
    curency_salary = curency_salary.replace(' ', '')
        # # Ссылку на саму вакансию.
    p = vacancy.find_all('a',{'class','bloko-link'})
    paragraphs = []
    for x in p:
        paragraphs.append(str(x))

    a = re.findall(r'(?P<url>https?://[^\s]+)', paragraphs[0])
    link_vacancy = a[0]
        # Сайт, откуда собрана вакансия.
    link_source = 'https://hh.ru'


    vacancy_data['name'] = name
    vacancy_data['min_salary'] = min_salary
    vacancy_data['max_salary'] = max_salary
    vacancy_data['curency_salary'] = curency_salary
    vacancy_data['link_vacancy'] = link_vacancy
    vacancy_data['link_source'] = link_source    

    vacancy_list.append(vacancy_data)

pprint(vacancy_list) 


# In[10]:



client = MongoClient('localhost', 27017)
db = client.test


vacancy = db.vacancy

db_mongo = vacancy.find({})
comper_mongodb = []
for i in db_mongo:
        ac=re.findall(r'\d+', i['link_vacancy'])
        comper_mongodb.append(ac[0])
   
print(len(comper_mongodb))


# In[9]:


for i in vacancy_list:
    e = re.findall(r'\d+', i['link_vacancy'])
    if e[0] not in comper_mongodb:
        vacancy.insert_one(i)

