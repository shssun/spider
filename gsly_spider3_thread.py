import requests
from bs4 import BeautifulSoup
from collections import deque
from multiprocessing.dummy import Pool as ThreadPool

queue = deque()
visited = set()
errors = []
count = 0


rootURL = 'http://www.gsly.gov.cn/'
queue.append(rootURL)


while queue:
    try:
        url = queue.popleft()
        visited.add(url)
        res = requests.get(url)
        if not res.status_code == 200:
            error = {}
            error['code'] = res.status_code
            error['url'] = url
            print('##############  页面读取错误, 错误代码{}, url = {}  ##################', error['code'], error['url'])
            errors.append(error)
            continue
        res.encoding = 'utf8'
        resDom = BeautifulSoup(res.text, 'html.parser')
        aList = resDom.select('a')
        for a in aList:
            try:
                href = str(a['href']).strip()
            except:
                continue
            try:
                title = str(a['title']).strip()
            except:
                title = a.text
            # 如果取出来的链接是以根域名开头, 并且没有被访问过, 则加到队列queue中
            if href.startswith(rootURL) and href not in visited and href not in queue:
                queue.append(href)
                count += 1
                print('抓取长链接{}: {} | {} | 父目录: {}'.format(count, title, href, url))
                continue
            # 如果取出来链接是短链接, 也即不是http开头的链接, 或者不是javascript开头的链接, 则根域名和并短连接, 构建完整的长链接
            if not href.startswith('http') and not href.startswith('javascript') and not href.startswith('#') and not href.startswith('mailto:') and (rootURL + href).replace('cn//','cn/') not in visited and (rootURL+href).replace('cn//','cn/') not in queue:
                queue.append((rootURL+href).replace('cn//','cn/'))
                count += 1
                print('抓取短链接{}: {} | {} | 父目录: {}'.format(count, title, (rootURL + href).replace('cn//','cn/'), url))

    except:
       print('------------- 第 {} 抓取错误, 错误代码{}!  | 父目录:{}  ----------------'.format(count, url))
       continue

print('-----------最终结果-------------')
for error in errors:


    print('错误代码: {}, 对应链接为: {} ', error['code'], error['url'])
