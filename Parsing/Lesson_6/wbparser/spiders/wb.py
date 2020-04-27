# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import HtmlResponse
from wbparser.items import WbparserItem
from scrapy.loader import ItemLoader

class WbSpider(scrapy.Spider):
    name = 'wb'
    allowed_domains = ['leroymerlin.ru']
    #start_urls = ['https://www.wildberries.ru/catalog/0/search.aspx?kind=1&subject=105&search=%D0%BA%D1%80%D0%BE%D1%81%D1%81%D0%BE%D0%B2%D0%BA%D0%B8%20%D0%BC%D1%83%D0%B6%D1%81%D0%BA%D0%B8%D0%B5&sort=popular']

    def __init__(self, text):
        self.start_urls = [f'https://leroymerlin.ru/search/?q={text}']

    def parse(self,response:HtmlResponse):
        next_page = response.xpath("//a[@class='paginator-button next-paginator-button']/@href").extract_first()
        ads_links = response.xpath("//a[@class='black-link product-name-inner']/@href").extract()
        for link in ads_links:
            yield response.follow(link, callback=self.parse_product)
        yield response.follow(next_page, callback=self.parse)

    def parse_product(self,response:HtmlResponse):
        loader = ItemLoader(item=WbparserItem(), response=response)
        loader.add_xpath('name', "//h1/text()")
        loader.add_xpath('features', ("//dt[@class='def-list__term']/text()", "//dd[@class='def-list__definition']/text()"))
        loader.add_xpath('photos', "//img[@alt='product image']/@src")
        yield loader.load_item()

        #name = response.xpath("///h1/text()").extract_first()
        #photos = response.xpath("//img[@alt='product image']/@src").extract()
        #yield WbparserItem(name=name, photos=photos)

