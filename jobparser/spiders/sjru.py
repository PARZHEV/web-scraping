import scrapy
from scrapy.http import HtmlResponse
from jobparser.items import JobparserItem

class SupjobSpider(scrapy.Spider):
    name = 'supjob'
    allowed_domains = ['superjob.ru']
    start_urls = ['https://www.superjob.ru/resume/search_resume.html?keywords%5B0%5D%5Bkeys%5D=python&sbmit=1&t%5B0%5D=4',
                  'https://www.superjob.ru/resume/search_resume.html?keywords%5B0%5D%5Bkeys%5D=sales&sbmit=1&t%5B0%5D=4']

    def parse(self, response):
        next_page = response.xpath("//a[@class= 'icMQ_ bs_sM _3ze9n l9LnJ f-test-button-dalshe f-test-link-Dalshe']/@href").get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)
        links = response.xpath("//a[contains(@class,'icMQ_ YYC5F f-test-link')]/@href").getall()
        for link in links:
            yield response.follow(link, callback=self.vacancy_parse_sj)


    def vacancy_parse_sj(self, response: HtmlResponse):
        name = response.xpath("//h1[@class='mWAI4 _3DjcL _1tCB5 _3fXVo _2iyjv']/text()").get()
        salary = response.xpath("//span[@class='_3a-0Y _3DjcL _1tCB5 _3fXVo']/text()").get()
        url = response.url
        yield JobparserItem(name=name, salary=salary, url=url)
