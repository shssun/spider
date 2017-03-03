########################## 运行前必看！！！！！######################
########################## 版本 python3.5  ！！############################
# 要提前下载的库文件：
# 1.lxml               //pip install lxml
# 2.requests          //pip install requests
import requests
from lxml import etree
import re
from multiprocessing.dummy import Pool as ThreadPool  #这是一个多线程库，本程序开了四个线程，比一个线程速度要快3到4倍。

#   程序功能：爬取百度百科上面和python相关的1000个词条并输出到程序目录下的result.html文件之中去。
#   当然，你也可以把url链接改成你感兴趣的任何关键词链接，得到你想要的结果。
#   把url_count可以设置为任何数字，它是爬取页面的数量

# datas是最终爬取的title与content字典列表
# new_urls是1000个要爬取的url链接，它是不断增长的。
# 每一次抓取完一个页面链接，都要将这个链接从new_urls中移去，移去后的链接列表保存在less_urls之中。


datas = []
new_urls=[]
less_urls=[]
url_count = 10      #可以更改为任何大于1的值，看个人想爬取页面数量随意设置


#get_urls:给定一个特定的百科url，得到1000个urls的集合。
def get_urls():
    i=0
    while len(new_urls) < url_count:
        print("已有"+str(len(new_urls))+"个URL待爬取")
        url = less_urls[i]
        less_urls.pop(0)
        get_url(url)


def get_url(url):
    html = requests.get(url)
    html.encoding = "utf8"
    htmltext = html.text

    url_list = re.findall('/view/(.*?)htm', htmltext, re.S)  #用正则表达式查找页面所有的链接
    for url in url_list:
        complete_url = "http://baike.baidu.com/view/" + str(url) + "htm"
        if complete_url not in new_urls:
            new_urls.append(complete_url)
            less_urls.append(complete_url)


def crawl_single_page(url):
    try:
        data = {}
        html = requests.get(url)
        print("正在爬取 " + url)
        html.encoding = 'utf8'
        htmltext = html.text
        a = re.findall('"lemmaSummary">(.*?)<div class="basic-info', htmltext, re.S)
        selector = etree.HTML(str(a))
        info = selector.xpath('string(.)')
        content = info.replace('\\n', '').replace("['","").replace("']","")
        if len(content)==0:
            a= re.findall('"lemmaSummary">(.*?)<div class="lemmaWgt-lemmaCatalog">', htmltext, re.S)
            selector = etree.HTML(str(a))
            info = selector.xpath('string(.)')
            content = info.replace('\\n', '').replace(' ', '')
        selector1 = etree.HTML(htmltext)
        newtitle = selector1.xpath('// *[ @ id = "query"]/@value')
        title = newtitle[0]


        data['title'] = title
        data['content'] = content
        datas.append(data)
    except:
        print("error occured~")


if __name__=='__main__':


    url = "http://baike.baidu.com/view/21087.htm"   # 这是python词条的百科链接，这个url可以被更改为任何你感兴趣的链接

    new_urls.append(url)
    less_urls.append(url)
    get_urls()


    pool = ThreadPool(4)   #我开了四个线程
    results = pool.map(crawl_single_page, new_urls)
    pool.close()
    pool.join()
    print("正在写入文件：")
    fp=open('result.html','w',encoding='utf8')
    fp.write('<!DOCTYPE html>'+ '\n')
    fp.write('<html lang="en">' + '\n')
    fp.write('<head><meta charset="UTF-8"><title>python crawler result</title><style type="text/css">.tableclass{border:#000 1px solid;}.tableclass tr{border-bottom:#000 1px solid;border-right:#000 1px solid;}')
    fp.write(' .tableclass td{border-bottom:#000 1px solid;border-right:#000 1px solid;}</style></head>')
 
    fp.write('<body>' + '\n')
    fp.write('<table class="tableclass">' + '\n')
    for data in datas:
        if len(data['content']) > 2:
            fp.write('<tr>')
            fp.write('<td>%s</td>' % data['title'])
            fp.write('<td>%s</td>' % data['content'])
            fp.write('</tr>')
 
    fp.write('</table>' + '\n')
    fp.write('</body>' + '\n')
    fp.write('</html>' + '\n')
    fp.close()
    print("All the tasks Done Successfully!")