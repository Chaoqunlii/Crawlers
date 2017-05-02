import scrapy
from ..items import PornItem
import requests
import os
from pymongo import MongoClient
import datetime

class PornSpider(scrapy.Spider):
    '''This is the scrapy crawler of the web "http://www.porn.com" '''
    name = 'PornSpider'
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'}
    domain = 'https://www.porn.com/'
    categories = [
        # 'amateur', 'anal-fisting', 'anal-sex', 'anime', 'arab', 'asian', 'ass-shaking', 'ass-spreading', 'ass-to-mouth', 'babysitter', 'bbw', 'behind-the-scenes', 
        # 'bi-sexual', 'big-ass', 'big-cock', 'big-tits', 'black',
        'blindfold', 'blonde', 'blowjob', 'bondage', 'brazilian', 'british', 'brunette', 'camel-toe', 'cartoon',
        'celebrity', 'cfnm', 'chubby', 'college', 'cosplay', 'cougar', 'couples', 'cowgirl', 'creampie', 'creampie-ass', 'cum-swapping', 'cumshots', 'deep-throat', 
        'doggy-style', 'double-blowjob', 'double-penetration', 'ethnic', 'face-sitting', 'family-roleplay', 'feet-massage', 'fingering', 'fishnet-stockings', 'food', 
        'footjob', 'french', 'gag', 'gangbang', 'gaping', 'german', 'glamour', 'glory-hole', 'granny', 'group-sex', 'hairy-pussy', 'handjob', 'hardcore', 'hd', 'homemade',
        'hot-wax', 'indian', 'interracial', 'italian', 'japanese', 'kissing', 'korean', 'lactating', 'lap-dance', 'latex', 'latin', 'lesbian', 'licking', 'massage', 
        'masturbation', 'mature', 'midget', 'milf', 'missionary', 'nurse', 'oil-lotion', 'party', 'piledriver', 'police', 'pov', 'pregnant', 'public-flashing', 
        'pussy-fisting', 'pussy-spreading', 'redhead', 'reverse-cowgirl', 'russian', 'scissoring', 'shaved-pussy', 'shaving', 'sixty-nine', 'small-cocks', 'small-tits', 
        'smoking', 'solo', 'spanking', 'spitting', 'spoon', 'spreadeagle', 'squirting', 'strap-on', 'stripping', 'swedish', 'teen', 'thai', 'threesomes', 'titty-fucking', 
        'toys', 'transsexual', 'turkish',
        ]

    # def start_requests(self):
    #     url = 'https://www.porn.com/pictures/'
    #     yield scrapy.Request(url, callback=self.parse, headers=self.headers)

    def __init__(self):
        client = MongoClient()
        db = client['porn_crawl']
        self.porn_crawl_collection = db['porn']


    def start_requests(self):
        '''Find the entrance of each category from the index page.'''
        for category in self.categories:
            cateUrl = self.domain + 'pictures/' + category
            print(cateUrl)
            yield scrapy.Request(cateUrl, callback=self.parse, meta={'category': category}, headers=self.headers)
    
    def parse(self, response):
        # print('~~~~~~~~~~~~~~~~~~~~~~~~')
        # print(response.meta)
        category = response.meta['category']

        pathRoot = 'D:\\porns\\'
        path = pathRoot + category
        if not os.path.exists(path):
            os.mkdir(path)
        os.chdir(path)

        imgsUrls = response.xpath('//ul[@class="listThumbs pictures"]/li/a/@href').extract()
        for imgsUrl in imgsUrls:
            imgsUrl = imgsUrl[1:]
            imgsUrl_ = self.domain + imgsUrl 
            print(imgsUrl_)

            yield scrapy.Request(imgsUrl_, callback=self.imgsParse, headers=self.headers, meta={'category': category})

        nextPages = response.xpath('//a[@class="btn nav"]/@href').extract()
        nextPage = nextPage_ = None

        for next in nextPages:
            nextPage = next
        
        if nextPage != None:
            nextPage = nextPage[1:]
            nextPage_ = self.domain + nextPage
            print(nextPage)
            yield scrapy.Request(nextPage_, callback=self.parse, headers=self.headers, meta={'category': category})
        


    def imgsParse(self, response):

        item = PornItem()
        category = response.meta['category']
        files = response.xpath('//ul[@class="listPics"]/li/a/img/@src').extract()
        i = 0
        b = []
        

        imgsUrl = response.url
    
        # 去重
        if self.porn_crawl_collection.find_one({'GroupUrl': imgsUrl}):
            print('This picutres group has been crawled.')
        else:
            post = {
                'Category': category,
                'GroupUrl': imgsUrl,
                'Time': datetime.datetime.now()
            }
            self.porn_crawl_collection.save(post)


            if requests.get(files[0].replace('thumbnails/', '')).status_code == 200:
                while i < len(files):
                    a = files[i].replace('thumbnails/', '')
                    b.append(a)
                    i += 1
                item['file_urls'] = b
            else:
                item['file_urls'] = files

            item['file_paths'] = category
            print(item['file_urls'])

            for file_url in item['file_urls']:
                name = file_url[24:].replace('/', '_')
                with open(name, 'wb') as f:
                    f.write(requests.get(file_url).content)
            



        # yield item
