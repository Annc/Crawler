#coding=utf-8
from lxml import html
import requests
import threading
import sqlite3
requests.packages.urllib3.disable_warnings()
proxies = {
    'http' : "http://127.0.0.1:8888",
    'https' : "https://127.0.0.1:8888",
    #'http': "socks5://127.0.0.1:1080",
    #'https': "socks5://127.0.0.1:1080"
}

gErrCnt = 0
gLock = threading.Lock()

def getTree(urladr):
    r = requests.get(url=urladr,proxies=proxies, verify=False)
    tree = html.fromstring(r.text)
    return tree

def get_and_save_image(image, s):
    picLink = image.get('src')
    if picLink:
        pi = requests.get(picLink,timeout=60,proxies=proxies, verify=False)
        pic = pi.content
        with open(picpath + s + '.jpg', 'wb')as f:
            f.write(pic)
def get_page(urladress,cur):
    global gErrCnt
    header = {
        "Accept-Language": "zh-CN,zh;q=0.8,en;q=0.6",
    }
    tr = getTree(urladress)
    #得到主页面小图片的URL地址
    atables = tr.xpath("//a[@class='movie-box']")
    for ab in atables:
        href = ab.get('href')
        if href:
            #打开每一个小图片的地址
            tre = getTree(href)
            #得到编号
            mas = tre.xpath("//p/span")
            #得到该片的下载页面地址
            trs = tre.xpath('//a')
            for tr in trs:
                href = tr.get('href')
                if href:
                    if href.split('/')[-1] == mas[1].text:
                        downPageUrl = href
            print(downPageUrl)
            #打开下载页面
            rr = requests.get(url=downPageUrl,headers = header,proxies=proxies, verify=False)
            downpageTree = html.fromstring(rr.text)
            #得到class=row的超链接
            downurls = downpageTree.xpath("//div[@class='row']/a")
            if downurls:
                for downurl in downurls:
                    downhref = downurl.get('href')
                    print("A片下载地址:"+downhref+"\n")
                images = tre.xpath("//a[@class='bigImage']/img")
                cur.execute("INSERT INTO Aadrr VALUES('%s', 'not')" % (mas[1].text))
                cur.commit()
                cur.close()
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
        conn = sqlite3.connect('D:\\python\\db\\test.db')
        get_page(self.url,conn)

if __name__ == '__main__':
    tlist = []
    picpath = 'D:\\IMG\\'
    for i in range(1,3):
        adr = 'https://avmo.pw/cn/released/page/'+ str(i)
        tr = DwnClass(adr)
        tr.start()
        tlist.append(tr)
        print("thread : %d" % (i))
    for i in tlist:
        i.join()
    print("err cnt : %d" % (gErrCnt))
