#1) Развернуть у себя на компьютере/виртуальной машине/хостинге MongoDB и реализовать функцию, записывающую собранные вакансии в созданную БД
#2) Написать функцию, которая производит поиск и выводит на экран вакансии с заработной платой больше введенной суммы
#3*)Написать функцию, которая будет добавлять в вашу базу данных только новые вакансии с сайта

from pymongo import MongoClient
from pprint import pprint
import json

client = MongoClient('localhost', 27017)
db = client['database_312']
vacancies = db.vacancies

#---------------task_1-------------------

file ='hh_sj_parsing.json'

def load_in_db(file):
    with open(file) as json_file:
        data = json.load(json_file)
    vacancies.insert_many(data)
    print(vacancies.count_documents({}))

#load_in_db(file)

#---------------task_2-------------------

def find_salary(salary, currency):
    request = {'$and':[
        {'$or': [{'salary.exact': {'$gt': salary}}, {'salary.min': {'$gt': salary}}, {'salary.max': {'$gt': salary}}]},
        {'salary.currency': currency}
    ]}
    return request

#for vacancies in vacancies.find(find_salary(20000, 'руб.')):
#    pprint(vacancies)

#---------------task_3-------------------


