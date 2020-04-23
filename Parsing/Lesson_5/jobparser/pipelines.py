# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import re
from pymongo import MongoClient

class JobparserPipeline(object):
    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.mongo_base = client.vac312

    def process_item(self, item, spider):
        collection = self.mongo_base['vacancies']
        item['salary'] = {'min': None, 'max': None, 'currency': None}

        if item['source'] == 'hh.ru':
            if 'от ' in item['salary_cont'] and ' до ' in item['salary_cont']:
                item['salary']['min'] = item['salary_cont'][1]
                item['salary']['max'] = item['salary_cont'][3]
                item['salary']['currency'] = item['salary_cont'][5]
            elif 'от ' in item['salary_cont'] and ' до ' not in item['salary_cont']:
                item['salary']['min'] = item['salary_cont'][1]
                item['salary']['currency'] = item['salary_cont'][3]
            elif 'от ' not in item['salary_cont'] and 'до ' in item['salary_cont']:
                item['salary']['max'] = item['salary_cont'][1]
                item['salary']['currency'] = item['salary_cont'][3]

        elif item['source'] == 'superjob.ru':
            if 'от' not in item['salary_cont'] and 'до' not in item['salary_cont'] and 'По договорённости' not in item['salary_cont']:
                item['salary']['min'] = item['salary_cont'][0].replace(u'\xa0', u' ')
                item['salary']['max'] = item['salary_cont'][1].replace(u'\xa0', u' ')
                item['salary']['currency'] = item['salary_cont'][3]
            elif 'от' in item['salary_cont']:
                item['salary']['min'] = re.findall('(.+)\s\D+$', item['salary_cont'][2].replace(u'\xa0', u' '))[0]
                item['salary']['currency'] = re.findall('.+\s(\D+)$', item['salary_cont'][2].replace(u'\xa0', u' '))[0]
            elif 'до' in item['salary_cont']:
                item['salary']['max'] = re.findall('(.+)\s\D+$', item['salary_cont'][2].replace(u'\xa0', u' '))[0]
                item['salary']['currency'] = re.findall('.+\s(\D+)$', item['salary_cont'][2].replace(u'\xa0', u' '))[0]


        collection.insert_one(item)
        return item

