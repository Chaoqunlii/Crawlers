import requests
from bs4 import BeautifulSoup

url = 'http://hz.lianjia.com/ershoufang/pg/1/'
html = requests.get(url)
ul = BeautifulSoup(html.text, 'lxml').findAll(class_='clear')
for li in ul:
    print(li.content)