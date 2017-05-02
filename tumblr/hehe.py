from bs4 import BeautifulSoup
import requests
import os
import random
from redis import Redis

urls = [
        'https://hill108.tumblr.com/',
]

url = 'https://hill108.tumblr.com/page/1'

def request(url):
    header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'}
    proxies = {
        "http": "http://127.0.0.1:1080", 
        "https": 'https://127.0.0.1:1080'
    }
    print('requesting', url)
    html = requests.get(url, headers=header, proxies=proxies)
    return html.content

def soupBoiler(htmlConnt):
    soup = BeautifulSoup(htmlConnt, 'lxml')
    print('soupBoling')
    return soup

def imgParse(soup):
    os.chdir('D:\\Documents\\Python3\\tumblr\\images')

    imgs = soup.findAll('img')
    for img in imgs:
        imgConte = request(img['src'])
        tail = img['src'][-4:]
        imgName = img['src'][-20:-4].replace('/', '_')
        imgName = imgName.replace('.', '_')
        imgName = imgName + tail
        print('saving pic', imgName)
        with open(imgName, 'wb') as f:
            f.write(imgConte)


def all(url):
    i = url[-1:]
    print(i)
    content = request(url)
    soup = soupBoiler(content)
    imgParse(soup)

    i = int(i) + 1
    pageNum =  '/page/' + str(i)
    if soup.find('a', href=pageNum):
        print('find page next')
        url = str(url)[:-1] + str(i)
        all(url)


all(url)