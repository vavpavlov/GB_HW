#1) Необходимо собрать информацию о вакансиях на вводимую должность (используем input или через аргументы) с сайта superjob.ru и hh.ru.
# Приложение должно анализировать несколько страниц сайта(также вводим через input или аргументы). Получившийся список должен содержать в себе минимум:
#*Наименование вакансии
#*Предлагаемую зарплату (отдельно мин. отдельно макс. и отдельно валюту)
#*Ссылку на саму вакансию
#*Сайт откуда собрана вакансия
#По своему желанию можно добавить еще работодателя и расположение. Данная структура должна быть одинаковая для вакансий с обоих сайтов. Общий результат можно вывести с помощью dataFrame через pandas.

from pprint import pprint
from bs4 import BeautifulSoup as bs
import requests
import re
import json

headers = {'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36'}
vacancies = []


def hh_parsing(page, max_pages, hh_link, text, headers):
    i = 0
    while True:
        print(f'-------------------{page + 1}-----------------------')
        main_link = f'{hh_link}search/vacancy?area=&st=searchVacancy&text={text}&page={page}'
        response = requests.get(main_link, headers=headers).text
        soup = bs(response, 'lxml')
        super_button = soup.find('a', {'class': 'bloko-button HH-Pager-Controls-Next HH-Pager-Control'})
        main_data = soup.find('div', {'class': 'vacancy-serp'})
        for vacancy in main_data:
            vacancy_list = vacancy.find('div', {'class': 'vacancy-serp-item__row vacancy-serp-item__row_header'})
            if vacancy_list is not None:

                vacancy_data = {}
                vacancy_salary_data = {}
                vacancy_name = vacancy_list.find('span', {'class': 'g-user-content'}).getText()
                vacancy_link = vacancy_list.find('span', {'class': 'g-user-content'}).findChild()['href']
                vacancy_salary = vacancy_list.find('span', {'data-qa': 'vacancy-serp__vacancy-compensation'})
                if vacancy_salary is not None:

                    if re.findall('^(\s\d+\s\d+)', vacancy_salary.getText()):
                        vacancy_salary_data['exact'] = re.findall('^(\s\d+\s\d+)', vacancy_salary.getText())[0]
                        vacancy_salary_data['exact'] = int((vacancy_salary_data['exact']).replace(u'\xa0', u''))
                    else:
                        vacancy_salary_data['exact'] = None

                    if re.findall('от\s(\d+\s\d+)|(\d+\s\d+)-', vacancy_salary.getText()):
                        vacancy_salary_data['min'] = re.findall('от\s(\d+\s\d+)|(\d+\s\d+)-', vacancy_salary.getText())[
                            0]
                        vacancy_salary_data['min'] = list(filter(None, vacancy_salary_data['min']))[0]
                        vacancy_salary_data['min'] = int((vacancy_salary_data['min']).replace(u'\xa0', u''))
                    else:
                        vacancy_salary_data['min'] = None

                    if re.findall('до\s(\d+\s\d+)|.-(\d+\s\d+)', vacancy_salary.getText()):
                        vacancy_salary_data['max'] = \
                        re.findall('до\s(\d+\s\d+)|.-(\d+\s\d+)', vacancy_salary.getText())[0]
                        vacancy_salary_data['max'] = list(filter(None, vacancy_salary_data['max']))[0]
                        vacancy_salary_data['max'] = int((vacancy_salary_data['max']).replace(u'\xa0', u''))
                    else:
                        vacancy_salary_data['max'] = None

                    if re.findall('.+(руб.|USD|EUR)', vacancy_salary.getText()):
                        vacancy_salary_data['currency'] = re.findall('.+(руб.|USD|EUR)', vacancy_salary.getText())[0]
                    else:
                        vacancy_salary_data['currency'] = None

                else:
                    vacancy_salary_data = {'min': None, 'max': None, 'exact': None, 'currency': None}

                vacancy_data['name'] = vacancy_name
                vacancy_data['link'] = vacancy_link
                vacancy_data['salary'] = vacancy_salary_data
                vacancy_data['source_link'] = hh_link
                i += 1
                print(vacancy_data)
                vacancies.append(vacancy_data)

        if super_button is not None and page < max_pages - 1:
            page += 1
        else:
            break

    print(f'На сайте {hh_link} по запросу "{text}" найдено вакансий - {i}')

def sj_parsing(page, max_pages, sj_link, text, headers):
    i = 0
    while True:
        print(f'-------------------{page}-----------------------')
        main_link = f'{sj_link}/vacancy/search/?keywords={text}&page={page}'
        response = requests.get(main_link, headers=headers).text
        soup = bs(response, 'lxml')
        main_data = soup.find_all('div', {'class': 'iJCa5 _2gFpt _1znz6 _2nteL'})
        super_button = soup.find('a', {'class': 'icMQ_ _1_Cht _3ze9n f-test-button-dalshe f-test-link-Dalshe'})

        for vacancy in main_data:

            if vacancy.find('div', {'class': '_3mfro CuJz5 PlM3e _2JVkc _3LJqf'}) is not None:
                vacancy_data = {}
                vacancy_name = vacancy.find('div', {'class': '_3mfro CuJz5 PlM3e _2JVkc _3LJqf'}).getText()
                vacancy_link = vacancy.find('div', {'class': '_3mfro CuJz5 PlM3e _2JVkc _3LJqf'}).findChild()['href']
                vacancy_salary = vacancy.find('span', {
                    'class': '_3mfro _2Wp8I _31tpt f-test-text-company-item-salary PlM3e _2JVkc _2VHxz'}).getText()

                if vacancy_salary is not None:
                    vacancy_salary_data = {}
                    if re.findall('^(\s\d+\s\d+)', vacancy_salary):
                        vacancy_salary_data['exact'] = re.findall('^(\s\d+\s\d+)', vacancy_salary)[0]
                        vacancy_salary_data['exact'] = int((vacancy_salary_data['exact']).replace(u'\xa0', u''))
                    else:
                        vacancy_salary_data['exact'] = None

                    if re.findall('от\s(\d+\s\d+)|(\d+\s\d+)', vacancy_salary):
                        vacancy_salary_data['min'] = re.findall('от\s(\d+\s\d+)|(\d+\s\d+)', vacancy_salary)[0]
                        vacancy_salary_data['min'] = list(filter(None, vacancy_salary_data['min']))[0]
                        vacancy_salary_data['min'] = int((vacancy_salary_data['min']).replace(u'\xa0', u''))
                    else:
                        vacancy_salary_data['min'] = None

                    if re.findall('до\s(\d+\s\d+)|.-(\d+\s\d+)', vacancy_salary):
                        vacancy_salary_data['max'] = re.findall('до\s(\d+\s\d+)|(\d+\s\d+)', vacancy_salary)[0]
                        vacancy_salary_data['max'] = list(filter(None, vacancy_salary_data['max']))[0]
                        vacancy_salary_data['max'] = int((vacancy_salary_data['max']).replace(u'\xa0', u''))
                    else:
                        vacancy_salary_data['max'] = None

                    if re.findall('.+(руб.|USD|EUR)', vacancy_salary):
                        vacancy_salary_data['currency'] = re.findall('.+(руб.|USD|EUR)', vacancy_salary)[0]
                    else:
                        vacancy_salary_data['currency'] = None

                else:
                    vacancy_salary_data = {'min': None, 'max': None, 'exact': None, 'currency': None}

                vacancy_data['name'] = vacancy_name
                vacancy_data['link'] = sj_link + vacancy_link
                vacancy_data['salary'] = vacancy_salary_data
                vacancy_data['source_link'] = sj_link
                i += 1
                print(vacancy_data)
                vacancies.append(vacancy_data)

        if super_button is not None and page < max_pages:
            page += 1
        else:
            break

    print(f'На сайте {sj_link} по запросу "{text}" найдено вакансий - {i}')

hh_data = [0, 100, 'https://hh.ru/', 'python', headers]
sj_data = [1, 100, 'https://russia.superjob.ru', 'python', headers]

hh_parsing(*hh_data)
sj_parsing(*sj_data)

with open('hh_sj_parsing.json', 'w') as outfile:
    json.dump(vacancies, outfile)
#pprint(vacancies)

