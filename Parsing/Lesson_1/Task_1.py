import requests
import json
from pprint import pprint

user = input('Введите имя пользователя: ')

main_link = f'https://api.github.com/users/{user}/repos'
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36'}

response = requests.get(main_link, headers)
data = json.loads(response.text)

#pprint(data)

if response.ok:
    for resp in data:
        print(resp['name'], resp['html_url'])
else: print('Такого пользователя нет на GitHub')
