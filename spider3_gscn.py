import requests
import time
from bs4 import BeautifulSoup
from collections import deque
from multiprocessing.dummy import Pool as ThreadPool
import os,sys

# todo: 首页所有链接
# todo: 处理a中  javascript:void(0) 的问题
# todo: 首页中注释部分的超链接
# todo: 公用一个 visited set
# todo: 多线程
# todo: 处理flash中的链接
# todo: 结果按照要求保存在 文本/excel 文件中
# todo: 解决200代码,其实 是404的问题
# todo: 解决返回404,403, 任然可以点击打开页面的问题


def url_join(pre_fix='', sub_fix=''):
    if sub_fix is None:
        return
    if sub_fix.startswith('javascript'):
        return pre_fix
    if sub_fix is None or sub_fix == '#' or sub_fix == '/':
        return pre_fix
    if sub_fix.startswith('http'):
        return sub_fix
    if sub_fix.startswith('www'):
        return 'http://' + sub_fix
    if pre_fix.endswith('/') and sub_fix.startswith('/'):
        return pre_fix + sub_fix[1:]
    if pre_fix.endswith('/') or sub_fix.startswith('/'):
        return pre_fix + sub_fix
    else:
        return pre_fix + '/' + sub_fix


def checkHomePage(homePage):
    queue = deque()
    visited = set()
    errors = []
    count = 0

    res = requests.get(homePage)
    res.encoding = 'utf8'
    # 把首页解析为dom
    res_dom = BeautifulSoup(res.text, 'html.parser')


    # 处理首页上的img
    img_list = res_dom.select('img')
    for img in img_list:
        queue.append(url_join(homePage, img['src']))

    # 处理首页上的script
    script_list = res_dom.select('script')
    for script in script_list:
        if script.get('src') is None:
            continue
        queue.append(url_join(homePage, script.get('src')))

    # 处理首页上的a
    a_list = res_dom.select('a')

    for a in a_list:
        queue.append(url_join(homePage, a.get('href')))
    print(queue)
    fp = open(str(time.strftime('%Y-%m-%d')) + '.txt', 'w')
    fp.writelines('#################' + str(time.strftime('%Y-%m-%d')) + '#################' + '\n ')
    count = 0
    for q in queue:
        if q in visited:
            continue
        count += 1
        visited.add(q)
        try:
            res = requests.get(q)
        except:
            fp.writelines(str(count) + ' | 连接异常 | ' + q + '\n ')
        fp.writelines(str(count) + ' | ' + str(res.status_code) + ' | ' + q + '\n ')
        #print(str(count) + ' | ' + str(res.status_code) + ' | ' + q)
    fp.close()
    return

def checkDeadURL(rootURl):
    queue = deque()
    visited = set()
    errors = []
    count = 0

    queue.append(homePage)
    while queue:
        try:
            full_url = queue.popleft()
            info = full_url.split('|||')
            url = info[0]
            try:
                parent_url = info[-2]
            except:
                parent_url = ' '
            url_title = info[-1]
            visited.add(url)
            res = requests.get(url)
            if (not res.status_code == 200) or (len(res.text) < 1500):
                error = {}
                error['code'] = res.status_code
                error['url'] = url
                error['parent_url'] = parent_url
                error['title'] = url_title
                print('##############  页面读取错误, 错误代码{}, 标题是 : {} ,url = {} ,父url = {} ##################'.format(error['code'], error['title'], error['url']), error['parent_url'])
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
                if href.startswith(homePage) and href not in visited and href not in queue:
                    queue.append(href+'|||'+url+'|||'+title)
                    count += 1
                    print('抓取长链接{}: {} | {} | 父目录: {}'.format(count, title, href, url))
                    continue
                # 如果取出来链接是短链接, 也即不是http开头的链接, 或者不是javascript开头的链接, 则根域名和并短连接, 构建完整的长链接
                if not href.startswith('http') and not href.startswith('javascript') and not href.startswith('#') and not href.startswith('mailto:') and (homePage + href).replace('cn//','cn/') not in visited and (homePage+href).replace('cn//','cn/') not in queue:
                    queue.append((homePage+href).replace('cn//', 'cn/')+'|||'+url+'|||'+title)
                    count += 1
                    print('抓取短链接{}: {} | {} | 父目录: {}'.format(count, title, (homePage + href).replace('cn//','cn/'), url))

        except:
           print('------------- 第 {} 条抓取错误!  | 标题 : {} , url : {} , 父目录 : {}  ----------------'.format(count,  url_title, url, parent_url))
           continue

    print('-----------最终结果-------------')
    for error in errors:
        print('错误代码: {}, 对应链接为: {} '.format(error['code'], error['url']))


if __name__ == '__main__':
    homePage = 'http://www.gscn.com.cn/'
    checkHomePage(homePage)
    #checkDeadURL(homePage)

