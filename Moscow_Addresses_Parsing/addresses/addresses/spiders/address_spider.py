#response.css('table.regions_list a::attr(href)').get()
#response.css('div.double_part a::attr(href)').get()
#response.xpath('//html/body/div[1]/div[2]/p[3]/a/@title').extract()
#scrapy crawl address_spider -o addresses.csv -t csv

import scrapy
from fake_useragent import UserAgent
import pandas as pd

ua = UserAgent()
fake_user_agent = ua.random

class Spider(scrapy.Spider):
    name = 'address_spider'
    start_urls = ['http://mosopen.ru/streets']
    def parse(self, response):
        custom_settings = {"USER_AGENT": fake_user_agent}

        for region in response.css('table.regions_list a::attr(href)').extract():
            yield response.follow(region, callback=self.street_parse)
    def street_parse(self, response):
        for street in response.css('div.double_part a::attr(href)').extract():
            yield response.follow(street, callback=self.address_parse)
    def address_parse(self, response):
        for address in response.xpath('//html/body/div[1]/div[2]/p[3]/a/@title').extract():
            yield {'address' : address}
