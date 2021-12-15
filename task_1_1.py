#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# 1. Посмотреть документацию к API GitHub, разобраться как вывести список репозиториев для конкретного пользователя, 
# сохранить JSON-вывод в файле *.json.


# In[49]:


import requests
from pprint import pprint
import json

url = 'https://api.github.com/users/'
owner = 'PARZHEV' #PARZHEV конкретный пользователь кого хотим получить



response = requests.get(url+owner+'/repos')
j_data = response.json()

data = []
i = 0
for i in range(len(j_data)):
    a = j_data[i].get('full_name')
    data.append(a)


count_repo = []
i = 1
a = 0
for i in range(len(j_data)):
    a = a+1
    count_repo.append(a)

user_repos = dict(zip(count_repo, data))


with open('repos.json', 'w') as f:
    json.dump(user_repos, f)

