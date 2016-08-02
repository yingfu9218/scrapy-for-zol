# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json
import urllib, httplib, urlparse
import random


class ZolPipeline(object):
    def __init__(self):
        pass


    def process_item(self, item, spider):
        print  item['image_urls']
        savePath='./pic/'
        filelist = item['image_urls'].split('/')
        file=filelist[-1]
        urlopen = urllib.URLopener()
        fp = urlopen.open(item['image_urls'])
        data = fp.read()
        fp.close()
        file = open(savePath + file, 'w+b')
        file.write(data)
        file.close()
        return item
    def close_spider(self, item, spider):
        self.file.close()

