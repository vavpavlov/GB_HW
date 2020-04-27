# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import TakeFirst,MapCompose, Compose

def cleaner_photo(values):
    if values[:2] == '//':
        return f'http:{values}'
    return values


def gen_features(features):
    feat = features[:len(features)//2]
    feat_values = features[len(features)//2:]
    final_features = dict(zip(feat, feat_values))
    return final_features


class WbparserItem(scrapy.Item):
    # define the fields for your item here like:
    _id = scrapy.Field()
    name = scrapy.Field(output_processor=TakeFirst())
    features = scrapy.Field(input_processor=Compose(gen_features))
    photos = scrapy.Field(input_processor=MapCompose(cleaner_photo))
