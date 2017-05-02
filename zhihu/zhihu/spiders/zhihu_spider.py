import scrapy
from scrapy.selector import Selector
from bs4 import BeautifulSoup

class ZhihuSpider(scrapy.Spider):
    name = 'ZhihuSpider'
    header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'}
    def start_requests(self):
        urls = ['https://www.zhihu.com/question/26006703']

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse, headers=self.header)

    def parse(self, response):
        print(response.body.decode('utf-8'))

        print('/////////////////')
        # soup = BeautifulSoup(response.body, 'lxml')
        # print(soup)
        # items = soup.findAll('li', class_='item')
        
        with open('zhihu.html', 'w', encoding='utf-8') as f:
            f.write(response.body.decode('utf-8'))
        #     for item in items:
        #         print(item.text)
        #         print('en')

        #         f.write(item.text)
        #         f.write('\n')