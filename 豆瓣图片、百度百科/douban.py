# -*- coding:utf-8 -*-
import urllib.request
from urllib.request import urlopen
from urllib.error import HTTPError
from bs4 import BeautifulSoup
import requests
import os
import random
import time

# 设置本地保存地址
path = 'D:/doubanpics/'

urls = [
        # 'https://movie.douban.com/subject/1830528/photos?type=S&start=0&sortby=vote&size=a&subtype=a',
        # 'https://movie.douban.com/subject/26427831/photos?type=S&start=0&sortby=vote&size=a&subtype=a'
        # 'https://movie.douban.com/subject/1864810/photos?type=S&start=0&sortby=vote&size=a&subtype=a',
        # 'https://movie.douban.com/subject/4718246/photos?type=S&start=0&sortby=vote&size=a&subtype=a',
        # 'https://movie.douban.com/subject/2284418/photos?type=S&start=0&sortby=vote&size=a&subtype=a'
        # 'https://movie.douban.com/subject/2254648/photos?type=S&start=0',
        # 'https://movie.douban.com/subject/1863923/photos?type=S&start=0&sortby=vote&size=a&subtype=a',
        # 'https://movie.douban.com/subject/1830590/photos?type=S&start=0&sortby=vote&size=a&subtype=a',
        # 'https://movie.douban.com/subject/2157130/photos?type=S&start=0&sortby=vote&size=a&subtype=a',
        # 'https://movie.douban.com/subject/2153527/photos?type=S&start=0&sortby=vote&size=a&subtype=a'
        # 'https://movie.douban.com/subject/2239286/photos?type=S&start=0&sortby=vote&size=a&subtype=a',
        # 'https://movie.douban.com/subject/1786739/photos?type=S&start=00&sortby=vote&size=a&subtype=a',
        # 'https://movie.douban.com/subject/2156663/photos?type=S&start=0&sortby=vote&size=a&subtype=a',
        # 'https://movie.douban.com/subject/2153527/photos?type=S&start=0&sortby=vote&size=a&subtype=a',
        # 'https://movie.douban.com/subject/1830590/photos?type=S&start=0&sortby=vote&size=a&subtype=a',
        # 'https://movie.douban.com/subject/2270545/photos?type=S&start=0&sortby=vote&size=a&subtype=a',
        # 'https://movie.douban.com/subject/3103410/photos?type=S&start=0&sortby=vote&size=a&subtype=a',
        # 'https://movie.douban.com/subject/2157146/photos?type=S&start=40&sortby=vote&size=a&subtype=a',
        'https://movie.douban.com/subject/3901418/photos?type=S&start=0&sortby=vote&size=a&subtype=a',

        ]


for url in urls:
    # 进入urls的循环
    showName = url.split('/')[4]
    print(showName)
    folder = path + showName
    print(folder)
    if not os.path.exists(folder):
        os.mkdir(folder)
    os.chdir(folder)
    next = url
    while next:
        # ip = ''.join(str(random.choice(iplist)).strip())
        # ip_ = 'http://' + ip
        # proxies = {'http': ip_, 'https': ip_}
        # print(proxies)
        # proxy_support = urllib.request.ProxyHandler(proxy)
        # opener = urllib.request.build_opener(proxy_support)
        # urllib.request.install_opener(opener)
        try:
            # html = urllib.request.urlopen(next).read()
            html = requests.get(next)
            print(html.content.decode('utf-8'))
        except HTTPError as e:
            print(e)
        if html is None:
            print('this page is none')
        else:
            # print(html.decode('utf-8'))
            bsObj = BeautifulSoup(html.text, 'lxml')
            # print(bsObj.encode()) 
            imgs = bsObj.find('ul', class_='poster-col4').findAll('img')
            for img in imgs:
                imgUrl = img['src']
                if imgUrl.find('thumb'):
                    # 豆瓣上的小图命名为thumb， 将其替换为photo即可变为大图

                    imgUrl_ = imgUrl.replace('thumb', 'photo')
                    print(imgUrl_)
                    img_name = imgUrl.split('/')[7]
                    with open(img_name, 'wb') as f:
                        f.write(urlopen(imgUrl_).read())
                    time.sleep(1)
            try:
                next = bsObj.find('span', {'class':'next'}).find('a')['href']
                print(next)
            except:
                print(u'这个电视剧爬完了')

            