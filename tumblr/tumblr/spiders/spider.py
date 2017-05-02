import scrapy
from bs4 import BeautifulSoup
from tumblr.items import TumblrItem
import random
import time
import re
# from selenium import webdriver

class TumblrSpider(scrapy.Spider):
    name = 'tumblrSpider'
    header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'}
    # driver = webdriver.Chrome()


    def start_requests(self):
        urls = [
                # 'https://forgottenflowergirl.tumblr.com/page/1',
                # 'https://luoli-g.tumblr.com/',
                # 'https://luoli-g.tumblr.com/',
                # 'https://kocklrto.tumblr.com/',
                # 'https://luolita-luoli.tumblr.com/',
                # 'https://luolimiao.tumblr.com/',
                # 'https://5ifuli.tumblr.com/',
                # 'https://3377635257.tumblr.com/',
                # 'https://asdfhgj.tumblr.com/',
                'https://hill108.tumblr.com/',
                # 'https://luoli-l.tumblr.com/',
                # 'https://lu-oli.tumblr.com/',
                # 'https://ailuoli1314.tumblr.com/',
                # 'http://wczw.tumblr.com/'
                # 'http://sam2119931.tumblr.com/'
                
        ]
        for url in urls:
            url = url + 'api/read?num=1000'
            yield scrapy.Request(url=url, callback=self.parse, headers=self.header)

    
    def parse(self, response):
        str(response.body).replace('&lt;', '<').replace('&gt;', '>')

        # print(response.body)
        with open('tum3.html', 'w', encoding='utf-8') as f:
            f.write(response.body.decode('utf-8'))
        item = TumblrItem()

        files = response.xpath('//photo-url[@max-width="1280"]/text()').extract()
        # # files = response.xpath('//video-player').extract()
        # # for file in files:
        # i = 0
        # while i < len(files):
        #     # print(file)
        #     pattern = r'source src="(.*?)"'
        #     m_tr = re.findall(pattern, files[i], re.S|re.M)
        #     files[i] = m_tr
        #     files[i] = ','.join(files[i])
        #     i += 1
        #     # print(m_tr)
        #     # file = m_tr
        # # print(files)
        # # files = ','.join(str(file) for file in files) 
        print(files)
        item['file_urls'] = files
        print(item['file_urls'])
        yield item


