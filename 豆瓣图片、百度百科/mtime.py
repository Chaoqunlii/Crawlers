# -*- coding:utf-8 -*-
from urllib.request import urlopen
from urllib.error import HTTPError
from bs4 import BeautifulSoup
import os

path = 'D:/mtimepics/'
urls = ['http://movie.mtime.com/235430/posters_and_images/stills/hot.html']


for url in urls:
    showName = url.split('/')[3]
    print(showName)
    folder = path + showName
    print(folder)
    if not os.path.exists(folder):
        os.mkdir(folder)
    os.chdir(folder)
    next = url
    while next:
        try:
            html =urlopen(next).read()
        except HTTPError as e:
            print(e)
        if html is None:
            print('this page is none')
        else:
            # print(html.decode('utf-8'))
            bsObj = BeautifulSoup(html, 'lxml')
            # print(bsObj.encode()) 
            imgs = bsObj.find('ul', id='imageDiv').findAll('img')
            for img in imgs:
                imgUrl = img['src']
                if imgUrl.find('thumb'):
                    imgUrl_ = imgUrl.replace('thumb', 'photo')
                    print(imgUrl_)
                    img_name = imgUrl.split('/')[7]
                    with open(img_name, 'wb') as f:
                        f.write(urlopen(imgUrl_).read())
            next_ = bsObj.find('span', {'class':'next'}).find('a')['href']
            if next_:
                next = next_
                print(next)
            else:
                print(u'这个电视剧爬完了')

