import requests
from bs4 import BeautifulSoup
import os


urls = 'https://www.pornpics.com/ebony/'

class Porn:

    def __init__(self):
        self.headers = {
            "User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.104 Safari/537.36 Core/1.53.1836.400 QQBrowser/9.5.9947.400",
            "Connection":"keep-alive",
            "Upgrade-Insecure-Requests":"1",
        }
        self.domain_ = 'https://www.pornpics.com/'
        self.tags = ['amateur', 'anal', ' anal-gape', 'asian', 'ass', 'ass-fucking', 'ass-licking',
                'babe', 'ball-licking', 'bath', 'bbw', 'beach', 'big-cock', 'big-tits', 'bikini',
                'blindfold', 'blowbang', 'blowjog', 'bondage', 'boots', 'brunette', 'bukkake', 
                'centerfold', 'cfnm', 'cheerleader', 'christmas', 'cloase-up', 'clothed', 'college',
                'cosplay', 'cougar', 'cowgirl', 'creampie', 'cum-in-mouth', 'cum-in-pussy', 'cumshot',
                'latex', 'latina', 'legs', 'lesbian'
                ]
        self.rootPath = 'D:\\porns\\'
    def request(self, url):
        html = requests.get(url, headers=self.headers).content
        print('get html')
        return html

    def boil(self, html_content):
        soup = BeautifulSoup(html_content, 'lxml')
        print('boil soup')
        return soup
        
    def findImgs(self, soup):
        imgs = soup.findAll('img')
        print('get imgs')
        return imgs

    def saveImg(self, imgs):
        for img in imgs:
            imgName = img['src'].replace('/', '_')[-30:]
            print(img['src'])
            print('saving img')
            with open(imgName, 'wb') as f:
                f.write(requests.get(img['src']).content)

    def makePage(self, url):
        pass
    
    def main(self):
        for tag in self.tags:
            path = self.rootPath + tag + '\\'
            os.mkdir(path)
            os.chdir(path)


            domain = self.domain_ + tag + '/'
            statusCode = requests.get(domain, headers=self.headers).status_code
            self.saveImg(self.findImgs(self.boil(self.request(domain))))
            i = 2
            while True:
                urltail = domain.split('/')[3] + '-' + str(i) + '.shtml'
                url = domain + urltail

                statusCode = requests.get(url, headers=self.headers).status_code
                print(statusCode)
                if statusCode == 200:
                    html = self.request(url)
                    soup = self.boil(html)
                    imgs = self.findImgs(soup)
                    self.saveImg(imgs)
                else:
                    break
                i += 1



porn = Porn()
porn.main()

