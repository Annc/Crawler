#coding=utf-8
from lxml import html
import requests
import threading
import sqlite3
import time
requests.packages.urllib3.disable_warnings()
proxies = {
    'http' : "http://127.0.0.1:8888",
    'https' : "https://127.0.0.1:8888",
    #'http': "socks5://127.0.0.1:1080",
    #'https': "socks5://127.0.0.1:1080"
}
gErrCnt = 0
gLock = threading.Lock()
quan = []
def write_str(quan_str):
    with open('D:\\IMG\\addr.txt', 'a')as f:
        f.write(quan_str)
        f.close()
def getTree2(urladr):
    global gErrCnt
    header = {
        "Accept-Language": "zh-CN,zh;q=0.8,en;q=0.6",
    }
    try:
        r = requests.get(url=urladr,headers = header,proxies=proxies, verify=False,timeout=60)
        tree = html.fromstring(r.text)
        return tree
    except:
        gLock.acquire()
        gErrCnt = gErrCnt + 1
        gLock.release()

def getTree(urladr):
    global gErrCnt
    try:
        r = requests.get(url=urladr,proxies=proxies, verify=False,timeout=60)
        tree = html.fromstring(r.text)
        return tree
    except:
        gLock.acquire()
        gErrCnt = gErrCnt + 1
        gLock.release()

def get_and_save_image(image, s):
    picLink = image.get('src')
    if picLink:
        pi = requests.get(picLink,timeout=60,proxies=proxies, verify=False)
        pic = pi.content
        with open('D:\\IMG\\' + s + '.jpg', 'wb')as f:
            f.write(pic)
            f.close()
def get_page(urladress):
    global gErrCnt
    tr = getTree(urladress)
    time.sleep(10)
    #得到主页面小图片的URL地址
    atables = tr.xpath("//a[@class='movie-box']")
    for ab in atables:
        href = ab.get('href')
        if href:
            #打开每一个小图片的地址
            tre = getTree(href)
            time.sleep(10)
            #得到编号
            mas = tre.xpath("//p/span")
            #得到该片的下载页面地址
            trs = tre.xpath('//a')
            for tr in trs:
                href = tr.get('href')
                if href:
                    if href.split('/')[-1] == mas[1].text:
                        downPageUrl = href
            #print('下载: ' + downPageUrl)
            #打开下载页面
            downpageTree = getTree2(downPageUrl)
            time.sleep(2)

            #downpageTree = getTree2('https://btso.pw/search/ULT-129')
            #得到class=row的超链接
            downurls = None
            try:

                downurls = downpageTree.xpath("//div[@class='row']/a")
            except:
                gLock.acquire()
                gErrCnt = gErrCnt + 1
                gLock.release()
            if downurls:
                addrs = []
                for downurl in downurls:
                    downhref = downurl.get('href')
                    if downhref:
                        hh = getTree2(downhref)
                        time.sleep(2)
                        try:
                            seed = hh.xpath("//textarea[@id='magnetLink']")
                            addrs.append(seed[0].text)
                        except:
                            gLock.acquire()
                            gErrCnt = gErrCnt + 1
                            gLock.release()
                if addrs:
                    gLock.acquire()
                    quan.append(mas[1].text)
                    quan.append(addrs)
                    gLock.release()
                    images = tre.xpath("//a[@class='bigImage']/img")
                    try:
                        get_and_save_image(images[0], mas[1].text)
                    except:
                        gLock.acquire()
                        gErrCnt = gErrCnt + 1
                        gLock.release()


class DwnClass(threading.Thread):
    def __init__(self, url):
        super().__init__()
        self.url = url

    def run(self):
        get_page(self.url)

if __name__ == '__main__':
    #必须先创建数据库
    conn = sqlite3.connect('D:\\python\\db\\test.db')
    tlist = []
    for i in range(1,5):
        adr = 'https://avmo.pw/cn/released/page/'+ str(i)
        tr = DwnClass(adr)
        tr.start()
        tlist.append(tr)
        print("thread : %d" % (i))
    for i in tlist:
        i.join()
    print("err cnt : %d" % (gErrCnt))
    s2 = ''
    print(len(quan))
    for li in quan:
        if type(li) == list:
            s1 = ''
            for sa in li:
                write_str(sa + '\n')
                s1 = s1 + sa + '*'
            #将结果存入数据库
            conn.execute("INSERT into Aadrr(No,adrr)values(?,?)" ,(s2,s1))
            conn.commit()

        else:
            write_str(li + '\n')
            s2 = li

    conn.close()
