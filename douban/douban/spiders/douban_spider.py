from scrapy.spider import Spider
from douban.items import DoubanItem
from scrapy import Request
import re
from bs4 import BeautifulSoup
import time
class DoubanMovieTopSpider(Spider):
    name = 'douban_movie_top250'

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36',
    }

    def start_requests(self):
        url = 'https://movie.douban.com/top250'
        yield Request(url, headers=self.headers)

    def parse(self, response):
        item = DoubanItem()
        # print(response.text)
        # bsObj = BeautifulSoup(response.text, 'lxml')
        # print(bsObj.decode('utf-8'))
        # movies = bsObj.find(class_='grid_view').findAll('li')
        movies = response.xpath('//ol[@class="grid_view"]/li')
        for movie in movies:

            item['ranking'] = movie.xpath(
                './/div[@class="pic"]/em/text()').extract()[0]
            item['movie_name'] = movie.xpath(
                './/div[@class="hd"]/a/span[1]/text()').extract()[0]
            item['score'] = movie.xpath(
                './/div[@class="star"]/span[@class="rating_num"]/text()'
                ).extract()[0]
            item['score_num'] = movie.xpath(
                './/div[@class="star"]/span/text()').re(u'(\d+)人评价')[0]
            yield item
            
            print(item['movie_name'])
        

        next_url = response.xpath('//span[@class="next"]/a/@href').extract()
        if next_url:
            time.sleep(2)
            next_url = 'https://movie.douban.com/top250' + next_url[0]
            yield Request(next_url, headers=self.headers)
            print(next_url)
        else:
            print('hehehehee')