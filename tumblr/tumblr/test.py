import requests
url = 'https://qqqpppbbbddd.tumblr.com/archive/filter-by/video#_=_'
# proxies = {
#     'http': 'http://127.0.0.1:1080',
#     'https': 'https://127.0.0.1:1080'
# }
html = requests.get(url)
print(html.content)
with open('a.html', 'w') as f:
    f.write(html.content)