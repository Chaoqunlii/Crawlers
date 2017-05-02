# -*- coding:utf-8 -*-
import urllib.request, urllib.error
from bs4 import BeautifulSoup
import pandas as pd
import time

def Disguise():
    header = ('User-Agent','Mozilla/5.0 (Windows NT 10.0; WOW64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36')
    opener = urllib.request.build_opener()
    opener.addheaders = [header]
    urllib.request.install_opener(opener)

def Get_page(url, num):
    try:
        time.sleep(1)
        page = urllib.request.urlopen(url).read()
        soup = BeautifulSoup(page, 'lxml')
        print('Page %d has been crawled.' %num)
        return soup
    except urllib.error.HTTPError as e:
        if hasattr(e, 'code'):
            print('Error reason: ', e.code)
        if hasattr(e, 'reason'):
            print('Error reason', e.reason)

def Get_House_info(page):
    item = {}
    item['house_name'] = [i.get_text().strip().split('|')[0] for i in page.select('div[class="houseInfo"]')]
    item['house_type'] = [i.get_text().strip().split('|')[1] for i in page.select('div[class="houseInfo"]')]   # 房型，厅室
    item['house_area'] = [i.get_text().strip().split('|')[2] for i in page.select('div[class="houseInfo"]')]   # 房屋大小
    item['house_position'] = [i.get_text().strip() for i in page.select('div[class="positionInfo"]')]
    item['house_interest'] = [i.get_text().strip().split('/')[0] for i in page.select('div[class="followInfo"]')]  # 关注人数
    item['house_see'] = [i.get_text().strip().split('/')[1] for i in page.select('div[class="followInfo"]')]    #带看人数
    item['house_issuedate'] = [i.get_text().strip().split('/')[2] for i in page.select('div[class="followInfo"]')]    #发布时间
    item['house_price'] = [i.get_text().strip() for i in page.select('div[class="totalPrice"] span')]    #房价
    item['house_unit_price'] = [i.get_text().strip() for i in page.select('div[class="unitPrice"] span')]    #单位价格
    return pd.DataFrame(item)

def main():
    filename = 'D:/lianjia_old.csv'
    Disguise()
    house_data = []
    for pg in range(1, 101):
        lianjia_url = 'http://hz.lianjia.com/ershoufang/pg/' + str(pg) + '/'
        page = Get_page(lianjia_url, pg) 
        if len(page) > 0:
            house_info = Get_House_info(page)
            house_data.append(house_info)
    data = pd.concat(house_data, ignore_index=True)
    data.to_csv(filename, encoding='gbk', index=False)
    print('Write over')
if __name__ == '__main__':
    main()