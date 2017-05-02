#-*-coding:utf-8-*-
import requests
from urllib.request import urlopen
from bs4 import BeautifulSoup
import chardet

url='https://www.zhihu.com/people/excited-vczh/following'
header={'User-Agent':'Mozilla/5.0(WindowsNT10.0;Win64;x64)AppleWebKit/537.36(KHTML,likeGecko)Chrome/56.0.2924.87Safari/537.36'}
html=requests.get(url,headers=header).content

#print(chardet.detect(html.decode('utf-8')))
soup=BeautifulSoup(html,'lxml')
# print(html.decode('utf-8'))
# print(soup)
with open('soup.txt','w',encoding='utf-8') as f:
    f.write(str(html.decode('utf-8')))