import requests

url = 'http://www.gstv.com.cn'
page = requests.get(url)
print(page.status_code)
print(page.content)