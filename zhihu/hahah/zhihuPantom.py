#-*-coding:utf-8-*-
import requests
from urllib.request import urlopen
from bs4 import BeautifulSoup
import gzip
from selenium import webdriver
from pymongo import MongoClient
import re
import random

class zhihuSpider:
    
    def __init__(self):
        self.client = MongoClient()
        self.zhihu_db = self.client.zhihu_db
        self.zhihu_collection = self.zhihu_db.zhihu_collection
        self.zhihu_queue = self.zhihu_db.queue_collection


        self.browser = webdriver.PhantomJS()
        self.header={'User-Agent':'Mozilla/5.0(WindowsNT10.0;Win64;x64)AppleWebKit/537.36(KHTML,likeGecko)Chrome/56.0.2924.87Safari/537.36'}

        self.url = 'https://www.zhihu.com/people/zhu-xi-99-58/following'
        userqueue = {}
        userqueue['url'] = self.url
        userqueue['crawled'] = False
        if self.zhihu_queue.find_one('url', self.url) == None:
            self.zhihu_queue.insert(userqueue)

    def request(self, url):
        self.browser.get(url)
        # print(browser.page_source)


        soupGen = BeautifulSoup(self.browser.page_source, 'html.parser')
        if soupGen.find('svg', class_='Icon--male'):
            userGender = soupGen.find('svg', class_='Icon--male').get('class')[1]
        elif soupGen.find('svg', class_='Icon--female'):
            userGender = soupGen.find('svg', class_='Icon--female').get('class')[1]
        else:
            userGender = ''
        if soupGen.find('div', class_="ProfileHeader-expandButton"):
            self.browser.find_element_by_class_name("ProfileHeader-expandButton").click()
        # if self.browser.find_element_by_class_name("ProfileHeader-expandButton") is not None:
        #     self.browser.find_element_by_class_name("ProfileHeader-expandButton").click()
        soup = BeautifulSoup(self.browser.page_source, 'html.parser')
        # self.browser.close()
        
        return userGender, soup


    def saveUser(self, url, userGender, soup, collection): 
        # 查找用户信息并保存
        
        profileSoup = soup.find('div', class_='ProfileHeader-main')
        if profileSoup:
            print('hahahahhahhaa')
            print(profileSoup)
            print(url)
            print('正在查看这个用户的信息')
            user = {}
            user['url'] = url
            user['avaUrl'] = profileSoup.find('img', class_='Avatar')['src']
            user['name'] = profileSoup.find('span', class_='ProfileHeader-name').text
            userGender = str(userGender).replace('-', '')
            userGender = str(userGender).replace('Icon', '')
            if userGender:
                user['gender'] = userGender
            else:
                user['gender'] = ''

            if profileSoup.find('span', class_='ProfileHeader-headline'):
                user['intro'] =  profileSoup.find('span', class_='ProfileHeader-headline').text
            else:
                user['intro'] = ''

            if profileSoup.find(text=re.compile("居住地")):
                user['location'] = profileSoup.find(text=re.compile("居住地")).parent.next_sibling.text
            else:
                user['location'] = ''

            if profileSoup.find(text=re.compile("所在行业")):
                user['profession'] = profileSoup.find(text=re.compile("所在行业")).parent.next_sibling.text 
            else:
                user['profession'] = ''

            if profileSoup.find(text=re.compile("职业经历")):
                user['career'] = profileSoup.find(text=re.compile("职业经历")).parent.next_sibling.text 
            else:
                user['career'] = ''

            if profileSoup.find(text=re.compile("教育经历")):
                user['education'] = profileSoup.find(text=re.compile("教育经历")).parent.next_sibling.text 
            else:
                user['education'] = ''

            if profileSoup.find(text=re.compile("个人简介")):
                user['personal'] = profileSoup.find(text=re.compile("个人简介")).parent.next_sibling.text 
            else:
                user['personal'] = ''

            print(user['url'])
            print(user['avaUrl'])
            print(user['name'])
            print(user['gender'])
            print(user['intro'])
            print(user['location'])
            print(user['profession'])
            print(user['career'])
            print(user['education'])
            print(user['personal'])

            if collection.find_one({'name': user['name']}) == None:
                print('正在保存ta')
                collection.insert(user)
            else:
                print('这个人已经爬过了~~')
        else:
            pass



    def seekNewUser(self, soup, userQueue):
        items = soup.findAll('div', class_='ContentItem')
        if items:
            for item in items:
                userLink = item.find('a', class_='UserLink-link')['href']
                userLink = 'https://www.zhihu.com' + str(userLink) + '/following'
                print(userLink)
                userDic = {}
                userDic['url'] = userLink
                userDic['crawled'] = False
                if userQueue.find_one({'url': userLink}) == None:
                    print('添加这个用户到待爬队列中。。。')
                    userQueue.insert(userDic)
                else:
                    print('这个用户已经添加到了队列中')

    

    def main(self):

        randomurl = self.zhihu_queue.find_one({'crawled': False})['url']

        while randomurl:
            print("url")
            print(randomurl)
            genAndSoup = self.request(randomurl)
            self.zhihu_queue.update({'url': randomurl}, {'$set': {'crawled': True}})
            gender = genAndSoup[0]
            # print(gender)
            soup = genAndSoup[1]
            # print(soup)
            self.saveUser(randomurl, gender, soup, self.zhihu_collection)
            self.seekNewUser(soup, self.zhihu_queue)

            randomurl = self.zhihu_queue.find_one({'crawled': False})['url']

if __name__ == '__main__':
    spider = zhihuSpider()
    spider.main()