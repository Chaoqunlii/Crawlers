# Required third party packages:
#     requests
#     BeautifulSoup
#     html5lib
import threading
import requests
import random
import time
from bs4 import BeautifulSoup
#启动画面
startpage = '''
爬虫 - 抓取知乎用户数据
'''
#多线程运行函数类
class ObtainResourceAsync(threading.Thread):
    def __init__(self, f, keyarg):
        threading.Thread.__init__(self)
        self.fun = f
        self.keyarg = keyarg
    def run(self):
        self.fun(**self.keyarg)
class writejson:
    def __init__(self, directory):
        self.directory = directory
    def readjson(self):
        temp = []
        with open(self.directory + '/data.json', 'r', encoding='utf8') as f:
            while True:
                data = f.readline()
                if (data != '\n') and (data != ''):
                    temp.append(json.loads(data[:-1]))
                else:
                    return temp
    def find(self):
        return self.readjson()
    def find_one(self, queryword={}, skip=0):
        if queryword != {}:
            for tmp in self.readjson():
                if list(queryword.keys())[0] in tmp:
                    if tmp[list(queryword.keys())[0]] == queryword[list(
                            queryword.keys())[0]]:
                        return tmp
            return None
        else:
            return random.choice(self.readjson())
    def insert_one(self, data):
        with open(self.directory + '/data.json', 'a', encoding='utf8') as f:
            json.dump(data, f)
            f.write('\n')
    def count(self):
        return len(self.readjson())
class ZhiHuCrawler:
    #cookies 和 headers 具有时效性，注意更换
    cookies = dict(cookies_are='')
    header = {'User-Agent': ''}
    def __init__(self, userdatabase):
        #存储已经抓取的主页url
        self._alreadyurl = set()
        #存储将要抓取的所有主页url
        self._allurl = set()
        #存储已经抓取的用户个人信息
        self._allpersoninf = []
        #访问数据库的接口
        self.userdatabase = userdatabase
        #最大线程数量
        self.maxthreads = 4
        #最大递归深度
        self.maxrecdepth = 4
        #HTML分析失败最多重试次数
        self.analytrytimes = 5
        #连接失败最多重试次数
        self.connectiontrytimes = 5
        #退出抓取循环标志
        self._urlflag = False
        #退出写入循环标志
        self._completeflag = False
        #遍历url计数
        self.countnum = 0
        #抓取的URL计数
        self.countuser = 0
#为allurl生成数据(关注的人的个人主页URL)
    def suburl(self, personalurl, recdepth, connectiontrytimes):
        if (recdepth > 0) and (connectiontrytimes >= 0):
            try:
                r = requests.get(personalurl + '/followees',
                                 headers=self.header,
                                 cookies=self.cookies)
            except (TypeError, ConnectionResetError,
                    requests.packages.urllib3.exceptions.ProtocolError,
                    requests.exceptions.ConnectionError):
                if connectiontrytimes - 1 > 0:
                    print('ConnectionError: 断开连接!进行重试,还剩' + str(
                        connectiontrytimes - 1) + '次重试机会')
                elif connectiontrytimes - 1 == 0:
                    print('ConnectionError: 断开连接!进行最后一次重试')
                self.suburl(personalurl, recdepth, connectiontrytimes - 1)
            else:
                source = BeautifulSoup(r.text, "html5lib")
                for temp in source.body(
                        'div',
                        class_='zm-profile-card zm-profile-section-item zg-clear no-hovercard'):
                    url = temp.find('a', class_='zg-link')['href']
                    self.countnum += 1
                    if url not in self._alreadyurl:
                        print('发现新用户! */' + url[28:])
                        self._allurl.add(url)
                    else:
                        print('已存在用户: */' + url[28:])
                    self.suburl(url, recdepth - 1, connectiontrytimes)
        elif connectiontrytimes < 0:
            print('最后一次重试失败!放弃尝试重新连接!')
#从个人主页URL获得个人信息
    def personalInformation(self, url, connectiontrytimes, analytrytimes):
        if (connectiontrytimes >= 0) and (analytrytimes >= 0):
            try:
                r = requests.get(
                    url + '/about', headers=self.header, cookies=self.cookies)
            except (TypeError, ConnectionResetError,
                    requests.packages.urllib3.exceptions.ProtocolError,
                    requests.exceptions.ConnectionError):
                if connectiontrytimes - 1 > 0:
                    print('ConnectionError: 断开连接!进行重试,还剩' + str(
                        connectiontrytimes - 1) + '次重试机会')
                elif connectiontrytimes - 1 == 0:
                    print('ConnectionError: 断开连接!进行最后一次重试')
                return self.personalInformation(url, connectiontrytimes - 1,
                                                analytrytimes)
            else:
                source = BeautifulSoup(r.text, "html5lib")
                PI = {}
                PI['主页'] = url
                try:
                    PI['姓名'] = source.find(
                        'div', class_='title-section ellipsis').a.string
                #有一定概率出现AttributeError异常，但重试之后不会出现，原因未知
                except AttributeError:
                    if analytrytimes - 1 > 0:
                        print('HTML分析错误!进行重试,还剩' + str(analytrytimes - 1) +
                              '次重试机会')
                    elif analytrytimes - 1 == 0:
                        print('HTML分析错误!进行最后一次重试')
                    return self.personalInformation(url, connectiontrytimes,
                                                    analytrytimes - 1)
                else:
                    f = lambda x: x['title'] if x != None else ''
                    PI['行业'] = f(source.find('span', class_='business item'))
                    PI['住址'] = f(source.find('span', class_='location item'))
                    PI['公司'] = f(source.find('span', class_='employment item'))
                    PI['职位'] = f(source.find('span', class_='position item'))
                    PI['学校'] = f(source.find('span', class_='education item'))
                    PI['专业'] = f(
                        source.find(
                            'span', class_='education-extra item'))
                    genders = source.find('span', class_='item gender')
                    if genders:
                        if genders.i['class'][1] == 'icon-profile-male':
                            PI['性别'] = '男'
                        elif genders.i['class'][1] == 'icon-profile-female':
                            PI['性别'] = '女'
                    else:
                        PI['性别'] = ''
                    return PI
        elif connectiontrytimes < 0:
            print('最后一次重试失败!放弃尝试重新连接!')
            return None
        elif analytrytimes < 0:
            print('最后一次重试失败!放弃尝试重新分析!')
            return None
#多线程获取所有个人信息
    def obtainAllpersoninf(self, lock):
        while True:
            if not self._urlflag:
                time.sleep(0.1)
            try:
                url = self._allurl.pop()
            except KeyError:
                if self._urlflag:
                    break
            else:
                ifflag = False
                lock.acquire()
                try:
                    if url not in self._alreadyurl:
                        self._alreadyurl.add(url)
                        ifflag = True
                finally:
                    lock.release()
                if ifflag:
                    print('抓取用户详细信息... ')
                    temp = self.personalInformation(
                        url, self.connectiontrytimes, self.analytrytimes)
                    if temp != None:
                        print('新用户数据成功抓取')
                        self._allpersoninf.append(temp)
#读取数据库中已有的主页
    def readalreadyurl(self):
        for tmp in self.userdatabase.find():
            self._alreadyurl.add(tmp['主页'])
    def writedata(self):
        while True:
            if not self._completeflag:
                time.sleep(0.1)
            try:
                personaldata = self._allpersoninf.pop()
            except IndexError:
                if self._completeflag:
                    break
            else:
                self.userdatabase.insert_one(personaldata)
                self.countuser += 1
                if not self._completeflag:
                    print('新用户录入数据库成功')
#初始化并启动多线程抓取URL
    def startUrlThreads(self, threadnum, threads, randomurl, recdepth):
        for i in range(threadnum):
            keyarg = {'personalurl': randomurl(),
                      'recdepth': recdepth,
                      'connectiontrytimes': self.connectiontrytimes}
            threads.append(ObtainResourceAsync(self.suburl, keyarg))
            threads[i].start()
#初始化并启动多线程抓取用户详细信息
    def startPIThreads(self, threadnum, threads, lock):
        for i in range(threadnum):
            keyarg = {'lock': lock}
            threads.append(
                ObtainResourceAsync(self.obtainAllpersoninf, keyarg))
            threads[i].start()
    def main(self):
        self._alreadyurl = set()
        self._allurl = set()
        self._allpersoninf = []
        self._urlflag = False
        self._completeflag = False
        self.countnum = 0
        self.countuser = 0
        urlthreads = []
        PIthreads = []
        #多线程锁
        lock = threading.Lock()
        recdepth = int(input('递归深度(最大递归深度' + str(self.maxrecdepth) +
                             '): ')) % (self.maxrecdepth + 1)
        if recdepth < 1:
            recdepth = 1
        threadnum = int(input('启用线程数量(最大线程数量' + str(self.maxthreads) +
                              '): ')) % (self.maxthreads + 1)
        if threadnum < 1:
            threadnum = 1
        self.connectiontrytimes = int(input('连接失败重试次数: '))
        if self.connectiontrytimes < 1:
            self.connectiontrytimes = 5
        self.analytrytimes = int(input('HTML分析失败重试次数: '))
        if self.analytrytimes < 1:
            self.analytrytimes = 5
        print('!!!!!读取数据库中已有用户主页URL!!!!!')
        self.readalreadyurl()
        print('!!!!!读取完毕!!!!!')
        #没有针对 数据库/JSON文件 中无数据的情况进行处理
        randomurl = lambda: self.userdatabase.find_one(skip=random.randrange(self.userdatabase.count()))['主页']
        self.startUrlThreads(threadnum, urlthreads, randomurl, recdepth)
        self.startPIThreads(threadnum // 4 + 1, PIthreads, lock)
        writedata = threading.Thread(target=self.writedata)
        writedata.start()
        for temp in urlthreads:
            temp.join()
        self._urlflag = True
        for temp in PIthreads:
            temp.join()
        self._completeflag = True
        writedata.join()
        print('!!!!!所有数据已录入数据库!!!!!')
        print('遍历:' + str(self.countnum) + '条URL')
        print('录入' + str(self.countuser) + '条Document')
class ZhiHuCrawlerTiny:
    #cookies 和 headers 具有时效性，注意更换
    cookies = dict(cookies_are='')
    header = {'User-Agent': ''}
    def __init__(self, userdatabase):
        #访问数据库的接口
        self.userdatabase = userdatabase
        #最大线程数量
        self.maxthreads = 4
        #最大递归深度
        self.maxrecdepth = 4
        #HTML分析失败重试次数
        self.analytrytimes = 5
        #连接失败重试次数
        self.connectiontrytimes = 5
        #遍历url计数
        self.countallurl = 0
        #抓取成功的用户数量计数器
        self.count = 0
    def obtainData(self, personalurl, recdepth, connectiontrytimes, lock):
        if (recdepth > 0) and (connectiontrytimes >= 0):
            try:
                r = requests.get(personalurl + '/followees',
                                 headers=self.header,
                                 cookies=self.cookies)
            except (TypeError, ConnectionResetError,
                    requests.packages.urllib3.exceptions.ProtocolError,
                    requests.exceptions.ConnectionError):
                if connectiontrytimes - 1 > 0:
                    print('ConnectionError: 断开连接!进行重试,还剩' + str(
                        connectiontrytimes - 1) + '次重试机会')
                elif connectiontrytimes - 1 == 0:
                    print('ConnectionError: 断开连接!进行最后一次重试')
                self.obtainData(personalurl, recdepth, connectiontrytimes - 1,
                                lock)
            else:
                source = BeautifulSoup(r.text, "html5lib")
                for temp in source.body(
                        'div',
                        class_='zm-profile-card zm-profile-section-item zg-clear no-hovercard'):
                    url = temp.find('a', class_='zg-link')['href']
                    self.countallurl += 1
                    lock.acquire()
                    try:
                        if self.userdatabase.find_one({'主页': url}) == None:
                            print('发现新用户! */' + url[28:])
                            PI = self.personalInformation(
                                url, self.connectiontrytimes,
                                self.analytrytimes)
                            if PI != None:
                                self.count += 1
                                print(
                                    '成功抓取第' + str(self.count) +
                                    '个用户,正在录入数据库...',
                                    end=' ')
                                self.userdatabase.insert_one(PI)
                                print('录入完成!')
                        else:
                            print('已存在用户: */' + url[28:])
                    finally:
                        lock.release()
                    self.obtainData(url, recdepth - 1, connectiontrytimes,
                                    lock)
        elif connectiontrytimes < 0:
            print('最后一次重试失败!放弃尝试重新连接!')
#从个人主页URL获得个人信息
    def personalInformation(self, url, connectiontrytimes, analytrytimes):
        if (connectiontrytimes >= 0) and (analytrytimes >= 0):
            try:
                r = requests.get(
                    url + '/about', headers=self.header, cookies=self.cookies)
            except (TypeError, ConnectionResetError,
                    requests.packages.urllib3.exceptions.ProtocolError,
                    requests.exceptions.ConnectionError):
                if connectiontrytimes - 1 > 0:
                    print('ConnectionError: 断开连接!进行重试,还剩' + str(
                        connectiontrytimes - 1) + '次重试机会')
                elif connectiontrytimes - 1 == 0:
                    print('ConnectionError: 断开连接!进行最后一次重试')
                return self.personalInformation(url, connectiontrytimes - 1,
                                                analytrytimes)
            else:
                source = BeautifulSoup(r.text, "html5lib")
                PI = {}
                PI['主页'] = url
                try:
                    PI['姓名'] = source.find(
                        'div', class_='title-section ellipsis').a.string
                #有一定概率出现AttributeError异常，但重试之后不会出现，原因未知
                except AttributeError:
                    if analytrytimes - 1 > 0:
                        print('HTML分析错误!进行重试,还剩' + str(analytrytimes - 1) +
                              '次重试机会')
                    elif analytrytimes - 1 == 0:
                        print('HTML分析错误!进行最后一次重试')
                    return self.personalInformation(url, connectiontrytimes,
                                                    analytrytimes - 1)
                else:
                    f = lambda x: x['title'] if x != None else ''
                    PI['行业'] = f(source.find('span', class_='business item'))
                    PI['住址'] = f(source.find('span', class_='location item'))
                    PI['公司'] = f(source.find('span', class_='employment item'))
                    PI['职位'] = f(source.find('span', class_='position item'))
                    PI['学校'] = f(source.find('span', class_='education item'))
                    PI['专业'] = f(
                        source.find(
                            'span', class_='education-extra item'))
                    genders = source.find('span', class_='item gender')
                    if genders:
                        if genders.i['class'][1] == 'icon-profile-male':
                            PI['性别'] = '男'
                        elif genders.i['class'][1] == 'icon-profile-female':
                            PI['性别'] = '女'
                    else:
                        PI['性别'] = ''
                    return PI
        elif connectiontrytimes < 0:
            print('最后一次重试失败!放弃尝试重新连接!')
            return None
        elif analytrytimes < 0:
            print('最后一次重试失败!放弃尝试重新分析!')
            return None
#初始化并启动多线程
    def startThreads(self, threadnum, threads, randomurl, recdepth, lock):
        for i in range(threadnum):
            keyarg = {'personalurl': randomurl(),
                      'recdepth': recdepth,
                      'connectiontrytimes': self.connectiontrytimes,
                      'lock': lock}
            threads.append(ObtainResourceAsync(self.obtainData, keyarg))
            threads[i].start()
    def main(self):
        threads = []
        #多线程锁
        lock = threading.Lock()
        #重置计数器
        self.countallurl = 0
        self.count = 0
        recdepth = int(input('递归深度(最大递归深度' + str(self.maxrecdepth) +
                             '): ')) % (self.maxrecdepth + 1)
        if recdepth < 1:
            recdepth = 1
        threadnum = int(input('启用线程数量(最大线程数量' + str(self.maxthreads) +
                              '): ')) % (self.maxthreads + 1) - 1
        if threadnum < 0:
            threadnum = 0
        self.connectiontrytimes = int(input('连接失败重试次数: '))
        if self.connectiontrytimes < 1:
            self.connectiontrytimes = 5
        self.analytrytimes = int(input('HTML分析失败重试次数: '))
        if self.analytrytimes < 1:
            self.analytrytimes = 5
#没有针对 数据库/JSON文件 中无数据的情况进行处理
        randomurl = lambda: self.userdatabase.find_one(skip=random.randrange(self.userdatabase.count()))['主页']
        #注意，后台线程一定要先于当前线程执行
        print('!!!!!开始抓取!!!!!')
        self.startThreads(threadnum, threads, randomurl, recdepth, lock)
        self.obtainData(randomurl(), recdepth, self.connectiontrytimes, lock)
        for temp in threads:
            temp.join()
        print('遍历:' + str(self.countallurl) + '条URL')
        print('录入' + str(self.count) + '条Document')
        print('!!!!!任务完成!!!!!')
if __name__ == "__main__":
    from datetime import datetime
    print(startpage)
    answer = input('你是否使用数据库? 注: 不使用数据库将使用json文件.\n(Y/N): ')
    if (answer == 'Y') or (answer == 'y'):
        # 访问数据库的接口
        import pymongo
        from pymongo import MongoClient
        client = MongoClient()
        zhihu_db = client.zhihu_db
        zhihu_collection = zhihu_db.zhihu_collection
    else:
        import json
        zhihu_collection = writejson(input('请输入数据保存文件夹路径: '))
    while True:
        print('请选择代码方案:')
        print('    A.速度快(CPU,内存占用稍高)')
        print('    B.非常慢，留待修改为非阻塞')
        select = input()
        if (select == 'A') or (select == 'a'):
            #计时开始
            start = datetime.now()
            ZhiHuCrawler(zhihu_collection).main()
            #计时结束
            end = datetime.now()
            print('耗费时长：' + str(end - start))
            flaga = input('是否继续?(Y/N)')
            if (flaga != 'Y') and (flaga != 'y'):
                break
        elif (select == 'B') or (select == 'b'):
            #计时开始
            start = datetime.now()
            ZhiHuCrawlerTiny(zhihu_collection).main()
            #计时结束
            end = datetime.now()
            print('耗费时长：' + str(end - start))
            flagb = input('是否继续?(Y/N)')
            if (flagb != 'Y') and (flagb != 'y'):
                break
        else:
            print('无效选项!')