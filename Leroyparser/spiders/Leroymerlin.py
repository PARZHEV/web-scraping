import scrapy
from scrapy.http import HtmlResponse
from Leroyparser.items import LeroyparserItem
from scrapy.loader import ItemLoader

class LeroySpider(scrapy.Spider):
    name = 'leroymerlin'
    allowed_domains = ['leroymerlin.ru']


    def __init__(self, search):
        super().__init__()
        self.start_urls = [f'https://leroymerlin.ru/search/?q={search}&suggest=true']


    def parse(self, response: HtmlResponse):
        next_page = response.xpath("//a[contains(@aria-label,'Следующая страница')]/@href").get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)
        links = response.xpath("//a[@data-qa='product-name']")
        for link in links:
            yield response.follow(link, callback=self.parse_goods)

    def parse_goods(self, response: HtmlResponse):

        # name = response.xpath("//h1[@itemprop='name']/text()").get()
        # price = response.xpath("//span[@slot='price']/text()").getall()
        # photo = response.xpath("//img[contains(@slot,'thumbs')]/@src").getall()
        # url = response.url
        # yield LeroyparserItem(name=name, photo=photo, price=price, url=url)


        loader = ItemLoader(item=LeroyparserItem(), response=response)
        loader.add_xpath('name', "//h1[@itemprop='name']/text()")
        loader.add_xpath('price', "//span[@slot='price']/text()")
        loader.add_xpath('photo', "//img[contains(@slot,'thumbs')]/@src")
        loader.add_value('url', response.url)
        yield loader.load_item()




