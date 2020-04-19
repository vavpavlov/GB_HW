from lxml import html
import requests
from pprint import pprint
import re
import datetime
from pymongo import MongoClient
import json

client = MongoClient('localhost', 27017)
db = client['database_news']
news = db.news

file ='news_parsing.json'

def load_in_db(file):
    with open(file) as json_file:
        data = json.load(json_file)
    news.insert_many(data)
    print(news.count_documents({}))


now = datetime.datetime.now()
header = {'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36'}

result = []

def req_to_lenta():
    main_link = 'https://lenta.ru'
    try:
        response = requests.get(main_link,
                                headers=header)
        root = html.fromstring(response.text)
        items = root.xpath("//div[@class='b-yellow-box__wrap']/div[@class='item' and position()<5]")
        for item in items:
            dict = {}
            dict['link'] = main_link + item.xpath(".//a/@href")[0]
            dict['text'] = item.xpath(".//a//text()[1]")[0]
            int_responce = requests.get(dict['link'],
                                        headers=header)
            int_root = html.fromstring(int_responce.text)
            dict['data'] = int_root.xpath("//time[@class='g-date']/@datetime")[0]
            dict['source'] = 'Lenta.ru'
            result.append(dict)
    except Exception as e:
        print(e)
    return result

def req_to_mail():
    main_link = 'https://news.mail.ru'
    try:
        response = requests.get(main_link,
                                headers=header)
        root = html.fromstring(response.text)
        items = root.xpath("//ul[@class='list list_type_square list_overflow']/li[@class='list__item']")
        for item in items:
            dict = {}
            dict['text'] = item.xpath(".//a//text()")[0]
            dict['link'] = main_link + item.xpath(".//a/@href")[0]
            int_responce = requests.get(dict['link'],
                                headers=header)
            int_root = html.fromstring(int_responce.text)
            dict['source'] = int_root.xpath("//a[@class='link color_gray breadcrumbs__link']//text()")[0]
            dict['data'] = int_root.xpath("//span[@class='note__text breadcrumbs__text js-ago']/@datetime")[0]
            result.append(dict)
    except Exception as e:
        print(e)
    return result

def req_to_yandex():
    main_link = 'https://yandex.ru/news/'
    try:
        response = requests.get(main_link,
                                headers=header)
        root = html.fromstring(response.text)
        items = root.xpath("//div[@class='stories-set stories-set_main_no stories-set_pos_3']//td[@class='stories-set__item']")       #Внешние блоки, содержащие ссылку

        for item in items:
            dict = {}
            dict['link'] = 'https://yandex.ru' + item.xpath(".//a/@href")[0]
            dict['text'] = item.xpath(".//a//text()")[0]
            dict['source'] = re.findall('(.+)\s\d\d:\d\d' ,item.xpath(".//div[@class='story__date']//text()")[0])[0]
            dict['data'] = now.isoformat()
            result.append(dict)
    except Exception as e:
        print(e)
    return result

req_to_lenta()
req_to_mail()
req_to_yandex()

with open(file, 'w') as outfile:
    json.dump(result, outfile)

load_in_db(file)

pprint(result)


