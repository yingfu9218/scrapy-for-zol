# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from qidian.items import ZolItem
from  qidian.pipelines import ZolPipeline



class ZolSpider(scrapy.Spider):
    name = "Zol"
    allowed_domains = ["desk.zol.com.cn"]
    start_urls = (
        'http://desk.zol.com.cn/pc/',
        # 'http://desk.zol.com.cn/meinv/',
    )
    manurl="http://desk.zol.com.cn"

    def parse(self, response):
        nextpage= response.xpath('//*[@id="pageNext"]/@href').extract()[0]

        for onetitle in response.xpath('//*[@class="photo-list-padding"]'):
             title=onetitle.xpath('a/img/@alt').extract()[0]
             self.title=title
             url=self.manurl+onetitle.xpath('a/@href').extract()[0]
             yield scrapy.Request(url, callback=self.parse_one)
        if nextpage!="":
            nextpage=self.manurl+nextpage
            yield scrapy.Request(nextpage, callback=self.parse)
        pass
    # 进入每一个标题
    def parse_one(self, response):
        urls=response.xpath('//*[@id="showImg"]/li/a/@href').extract()
        for oneurl in urls:
            yield scrapy.Request(self.manurl+oneurl, callback=self.parse_onepic)
        pass
# 处理每一张图片，大小提取1366*768
    def parse_onepic(self,response):
        onepicurl=self.manurl+ response.xpath('//*[@id="1366x768"]/@href').extract()[0]
        # print onepicurl
        yield scrapy.Request(onepicurl, callback=self.parse_onepicurl)

    def parse_onepicurl(self,response):
        picurl=response.xpath('/html/body/img[1]/@src').extract()[0]
        # print picurl
        item = ZolItem()
        item['image_urls'] = picurl
        item['images'] = self.title
        return item
        pass





