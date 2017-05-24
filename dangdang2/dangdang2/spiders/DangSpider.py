# -*- coding:utf-8 -*-
__author__ = 'Windows'

import scrapy
from scrapy.http import Request
from dangdang2.items import Dangdang2Item

class DangSpider(scrapy.Spider):
    name = "dangdang"
    allowed_domains = ['dangdang.com']
    start_urls = ['http://3c.dangdang.com/pc']

    def parse(self,response):
        categroy = response.xpath('//div[@class="level_one "]/dl/dt/a/@href').extract()
        for url in categroy:
            yield Request(url, callback=self.parse_detail)

    def parse_detail(self, response):
        link = response.xpath('//a[@class="pic"]/@href').extract()
        if link:
            for detail_url in link:
                yield Request(detail_url, callback=self.parse_item)
            next_link = response.xpath('//li[@class="next"]/a/@href').extract()
            #print next_link
            if next_link:
                next_link = next_link[0]
                yield Request('http://category.dangdang.com'+next_link,callback=self.parse_detail)



    def parse_item(self,response):
        item = Dangdang2Item()

        item["title"]=response.xpath('//div[@class="name_info"]/h1/@title').extract()
        #print item['title'][0].encode('utf-8')

        item["comment_num"]=response.xpath('//a[@id="comm_num_down"]/text()').extract()
        #print item['comment_num']

        item["price"]=response.xpath('//p[@id="dd-price"]/text()').extract()
        #print item['price']

        item["link"]=response.url
        #print item['link']

        item["img_url"]=response.xpath('//img[@id="modalBigImg"]/@src').extract()
        #print item['img_url']

        yield item
