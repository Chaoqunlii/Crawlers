# -*- coding:utf-8 -*-

# 从百度百科上爬取关于角色介绍的内容


import urllib2
import requests
import os
from bs4 import BeautifulSoup
import sys
import json
type = sys.getfilesystemencoding()


# reload(sys)
# sys.setdefaultencoding('utf-8')


class baidupedia():
    def __init__(self):
        self.path = 'D:\\tvshow'
        self.urls = [
        			# 百度百科网址
                    # 'http://baike.baidu.com/item/%E4%B8%89%E7%94%9F%E4%B8%89%E4%B8%96%E5%8D%81%E9%87%8C%E6%A1%83%E8%8A%B1/16246274',
                    # 'http://baike.baidu.com/item/%E5%BE%AE%E5%BE%AE%E4%B8%80%E7%AC%91%E5%BE%88%E5%80%BE%E5%9F%8E/17698843',
                    # 'http://baike.baidu.com/item/%E8%8A%B1%E5%8D%83%E9%AA%A8/12813082',
                    # 'http://baike.baidu.com/item/%E9%9D%92%E4%BA%91%E5%BF%97/17545555',
                    # 'http://baike.baidu.com/item/%E7%94%84%E5%AC%9B%E4%BC%A0/4701562',
                    # 'http://baike.baidu.com/item/%E6%AC%A2%E4%B9%90%E9%A2%82/16954232',
                    # 'http://baike.baidu.com/item/步步惊心/10819206',
                    # 'http://baike.baidu.com/item/伪装者/15932508',
                    # 'http://baike.baidu.com/item/盗墓笔记/14492163',
                    # 'http://baike.baidu.com/item/大唐荣耀',
                    # 'http://baike.baidu.com/item/孤芳不自赏/17858522',
                    # 'http://baike.baidu.com/item/琅琊榜/12700172',
                    # 'http://baike.baidu.com/item/太子妃升职记/18264371',
                    # 'http://baike.baidu.com/item/轩辕剑之天之痕/61094',
                    # 'http://baike.baidu.com/item/仙剑奇侠传/5130936',
                    # 'http://baike.baidu.com/item/仙剑奇侠传三/5128963',
                    # 'http://baike.baidu.com/item/古剑奇谭/5016869',
                    # 'http://baike.baidu.com/item/锦绣未央/17043717',
                    # 'http://baike.baidu.com/item/大汉情缘之云中歌/3312504',
                    # 'http://baike.baidu.com/item/%E9%A3%8E%E4%B8%AD%E5%A5%87%E7%BC%98/15493209',
                    # 'http://baike.baidu.com/item/武媚娘传奇/16416130',
                    # 'http://baike.baidu.com/item/射雕英雄传/16723381',
                    # 'http://baike.baidu.com/item/神雕侠侣/5995778',
                    # 'http://baike.baidu.com/item/倚天屠龙记/7061269',
                    # 'http://baike.baidu.com/item/笑傲江湖/10719298',
                    # 'http://baike.baidu.com/item/天龙八部/5480164',
                    # 'http://baike.baidu.com/item/鹿鼎记/9411326'
                    # 'http://baike.baidu.com/item/%E4%BD%95%E4%BB%A5%E7%AC%99%E7%AE%AB%E9%BB%98/15839668',
                    # 'http://baike.baidu.com/item/%E6%97%A0%E5%BF%83%E6%B3%95%E5%B8%88/16997861',
                    # 'http://baike.baidu.com/item/%E8%8A%88%E6%9C%88%E4%BC%A0/73703',
                    # 'http://baike.baidu.com/item/%E9%AC%BC%E5%90%B9%E7%81%AF%E4%B9%8B%E7%B2%BE%E7%BB%9D%E5%8F%A4%E5%9F%8E/19171105',
                    # 'http://baike.baidu.com/item/%E9%99%86%E8%B4%9E%E4%BC%A0%E5%A5%87'
                    # 'http://baike.baidu.com/item/还珠格格/903367',
                    # 'http://baike.baidu.com/item/鹿鼎记/9411254',
                    # 'http://baike.baidu.com/item/小鱼儿与花无缺',
                    # 'http://baike.baidu.com/item/亮剑/10639926',
                    # 'http://baike.baidu.com/item/金粉世家/9285085',
                    # 'http://baike.baidu.com/item/三国演义/7088688',
                    # 'http://baike.baidu.com/item/康熙王朝/54309',
                    # 'http://baike.baidu.com/item/新白娘子传奇/419470',
                    # 'http://baike.baidu.com/item/水浒传/1442574',
                    # 'http://baike.baidu.com/item/西游记/6786341',
                    # 'http://baike.baidu.com/item/红楼梦/10578542',
                    # 'http://baike.baidu.com/item/%E5%AE%B0%E7%9B%B8%E5%88%98%E7%BD%97%E9%94%85/44923',
                    # 'http://baike.baidu.com/item/春光灿烂猪八戒/29506'，
                    # 'http://baike.baidu.com/item/封神榜之凤鸣岐山/'
                    'http://baike.baidu.com/item/孝庄秘史/29979'


            ]

    def mkdir(self, path):
    	# 创建本地保存文件夹
        isExisted = os.path.exists(path)
        if isExisted:
            print(u'这个角色或者电视剧已经爬过了')
            return False
        else:
            print(u'正在创建文件夹')
            os.makedirs(path)
            return True

    def request(self, url):
    	# http请求
        request = requests.get(url).content
        return request

    def get_soup(self, request):
    	# 对url请求后，进行BeautifulSoup处理

        soup = BeautifulSoup(request, 'lxml')
        return soup

    def main(self):
        if not self.mkdir(self.path):
            self.mkdir(self.path)
        
        os.chdir(self.path)
        for url in self.urls:
            

            request = self.request(url)
            soup = self.get_soup(request)
            tvname = soup.find(class_='lemmaWgt-lemmaTitle-title').h1.text
            roles = soup.find_all(class_='roleIntroduction-item')

            tv_path = self.path + '\\' + tvname.strip(' ')
            self.mkdir(tv_path)
            print(tv_path)
            for role in roles:
                name = role.find(class_='role-name').text
                name_ = ''
                if name.find('/'):
                    name_ = name.split('/')[0]    
                elif name.find('·'):
                    name_ = name.split('/')[0]    
                else:
                    name_ = name
                print('name_')
                # print name_

                description = role.find(class_='role-description').text
                # print description

                tvname_utf = tvname.strip().encode('utf-8')
                name_utf = name_.strip().encode('utf-8')
                description_utf = description.strip().encode('utf-8')

                # if tvname_utf.find(u'\xa0'):
                #     tvname_utf.replace(u'\xa0', u' ')
                # if name_utf.find(u'\xa0'):
                #     name_utf.replace(u'\xa0', u' ')
                # if description_utf.find(u'\xa0'):
                #     description_utf.replace(u'\xa0', u' ')
                
                role_folder = tv_path + '\\' + name_.strip()
                print(role_folder)
                self.mkdir(role_folder)
                
                os.chdir(role_folder)

                # 将所爬取到的内容保存到txt文件
                try:
                    txt_name = name_.strip() + '.txt'
                    print(txt_name)
                    print(tvname)
                    with open(txt_name, 'w') as f:
                        f.write(tvname_utf)
                        f.write('\n')
                        f.write(name_utf)
                        f.write('\n')
                        f.write(description_utf)
                except:
                    pass

instance = baidupedia()
instance.main()