from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

from Leroyparser.spiders.Leroymerlin import LeroySpider
from Leroyparser import settings

if __name__ == '__main__':
    crawler_settings = Settings()
    crawler_settings.setmodule(settings)

    process = CrawlerProcess(settings=crawler_settings)
    search = 'тумба'
    process.crawl(LeroySpider, search)
    process.start()

