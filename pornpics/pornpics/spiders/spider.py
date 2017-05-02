import scrapy
import requests
from ..items import PornpicsItem

class PornpicsSpider(scrapy.Spider):
    name = 'PSpider'
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'}

    handle_httpstatus_list = [404]

    def start_requests(self):
        urls = [
            # 'https://www.pornpics.com/face/'
            'https://www.pornpics.com/big-cock/'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse, headers=self.headers)

    def parse(self, response):
        print('parse, get statusCode~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
        yield scrapy.Request(url=response.url, callback=self.parse2, headers=self.headers)
        i = 2
        while True:

            url_tail = response.url.split('/')[3]
            url = response.url + str(url_tail) + '-' + str(i) + '.shtml'
            # print('Now wil test the address:')
            # print(url)
            code =  requests.get(url).status_code
            print('code:' + str(code)) 
            if code == 200:
                print('yieding Request to parse2')
                yield scrapy.Request(url=url, callback=self.parse2, headers=self.headers)
                i += 1
            else:
                print(str(code),'Can not crawl')
                break
    
    def parse2(self, response):
        print('Now parse2, saving pics。。。。。。。。。。。。。。。。。')
        # print(response.url)
        # item = PornpicsItem()
        # item['file_urls'] = response.xpath('//img/@src').extract()
        # print(item['file_urls'])
        # yield item
