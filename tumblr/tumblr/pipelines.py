# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import os
from scrapy.conf import settings
import scrapy
import requests
from scrapy.exceptions import DropItem
from scrapy.pipelines.images import ImagesPipeline
import time

class TumblrPipeline(object):
    def process_item(self, item, spider):
        # path = 'D:/Documents/Python3/tumblr'
        # content = requests.get(item['imgUrl'], proxies={'http': 'http://127.0.0.1:1080'}).content
        # content = scrapy.Request(item['imgUrl'])
        # name = item['imgUrl'][-15:]
        # with open(name, 'wb') as f:
        #     f.write(content)
        time.sleep(5)
        return item
    
# class TumblrPipeline(ImagesPipeline):
#     def get_media_requests(self,item,info):
#         for image_url in item['imgUrl']:
#             yield scrapy.Request(image_url)
#     def item_completed(self,results,item,info):
#         image_paths=[x['path'] for ok,x in results if ok]
#         if not image_paths:
#             raise DropItem('图片未下载好 %s'%image_paths)