# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class PornItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    file_paths = scrapy.Field()
    file_urls = scrapy.Field()
    file = scrapy.Field()