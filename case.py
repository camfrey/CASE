import scrapy


class CaseSpider(scrapy.Spider):
    name = 'case'
    allowed_domains = ['www.stackoverflow.com']
    start_urls = ['http://www.stackoverflow.com/']

    def parse(self, response):
        pass
