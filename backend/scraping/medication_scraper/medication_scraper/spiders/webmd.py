import scrapy


class WebmdSpider(scrapy.Spider):
    name = "webmd"
    allowed_domains = ["webmd.com"]
    start_urls = ["https://webmd.com/"]

    def parse(self, response):
        pass
