import requests
url = 'https://movie.douban.com/subject/26309788/'

html = requests.get(url)

print(html.content.decode('utf-8'))
with open('heh.txt','w') as f:
    f.write(str(html.content))