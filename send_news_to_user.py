from vk_api.longpoll import VkLongPoll, VkEventType
import vk_api
from datetime import datetime
import random
import time
import json
import requests

delta = 600
timetime = time.time() - delta

#subs = [293389676]
DB = open('DB','r')
subs = str(DB.read()).split()
DB.close()
print(subs)

url = 'https://newsapi.org/v2/top-headlines?pageSize=1&country=ru&apiKey=a78f940eef614cf6aaf33e6688e96dab'
last_new_title = ''
last_new_title = ((((requests.get(url)).json())['articles'])[0])['title']

token = "5331ac8225f18a756fa20a9fb0fc52569a168b4b8e4a02876bfa36d6582e344669e2bb128653d89e73777"
vk_session = vk_api.VkApi(token=token)

session_api = vk_session.get_api()
longpoll = VkLongPoll(vk_session)

while True:
    if (time.time()-timetime > delta):
      print("Отпраляю запрос! Время: "+str(time.time()))
      timetime = time.time()
      if ((((requests.get(url)).json())['articles'])[0])['title'] != last_new_title:

        DB = open('DB','r')
        subs = str(DB.read()).split()
        DB.close()
        print(subs)
        
        resp = (requests.get(url)).json()
        new_new = (resp['articles'])[0]
        if not(new_new['author']):
            new_new['author'] = '(не указан)'
        print("Новость отправлена:")
        for sub_id in subs:
            vk_session.method('messages.send', {'user_id': int(sub_id), 'message': new_new['title']+'\n \n'+new_new['description']+'\n ------ \n Источник: '+new_new['author']+'\n Подробнее: '+new_new['url'], 'random_id': 0})
            print(sub_id)
            
        last_new_title = new_new['title']
