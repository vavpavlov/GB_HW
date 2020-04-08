#Посмотреть документацию к API GitHub, разобраться как вывести список репозиториев для конкретного пользователя, сохранить JSON-вывод в файле *.json.

import requests
import json
from pprint import pprint

user = input('Введите имя пользователя: ')

main_link = f'https://api.github.com/users/{user}/repos'
headers = {'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36'}

response = requests.get(main_link, headers)
data = json.loads(response.text)

#pprint(data)

if response.ok:
    data_final = []
    data_final.append(user)

    print(f'Публичные репозитории пользователя {user} на GitHub:')

    for repos in data:
        print(repos['name'])
        data_final.append(repos['name'])

    with open(f'{user}_gh_pr.json', 'w') as outfile:
        json.dump(data_final, outfile)

else: print('Такого пользователя нет на GitHub')

