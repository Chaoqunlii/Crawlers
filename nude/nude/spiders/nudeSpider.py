import scrapy
from ..items import NudeItem 
class NudeSpider(scrapy.Spider):
    name = 'nudeSpider'
    domain = 'http://yuyongnian.com/'
    def start_requests(self):
        url = 'http://yuyongnian.com/p01/index.html'
        yield scrapy.Request(url)
        
    def parse(self, response):
        entrance = response.xpath('//div[@class="typelist"]//ul/li/a/@href').extract()
        for e in entrance:
            url = self.domain + e
            print(url)
            yield scrapy.Request(url, callback=self.parse_imgs_container)
        next = response.xpath('//a[@title="下一页"]/@href').extract()
        # next = response.xpath('//a[contains(text(), "下一页")]/@href').extract()
        if next:
            next = self.domain + next[0]
            print('next')
            print(next)
            yield scrapy.Request(next, callback=self.parse)
    
    def parse_imgs_container(self, response):
        item = NudeItem()
        item['file_urls'] = response.xpath('//div[@id="view1"]/img/@src').extract() 
        yield item