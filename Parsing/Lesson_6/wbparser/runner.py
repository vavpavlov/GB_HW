from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings
from wbparser import settings
from wbparser.spiders.wb import WbSpider

if __name__ == '__main__':
    crawler_settings = Settings()
    crawler_settings.setmodule(settings)
    process = CrawlerProcess(settings=crawler_settings)
    process.crawl(WbSpider, text='столешницы')

    process.start()