#coding:utf8
import sqlite3
import glob
import os
import requests
from lxml import html
requests.packages.urllib3.disable_warnings()
proxies = {
    'http' : "http://127.0.0.1:8888",
    'https' : "https://127.0.0.1:8888",
    #'http': "socks5://127.0.0.1:1080",
    #'https': "socks5://127.0.0.1:1080"
}
def do_post(urlAddr):
    #cookie是变化的
    header = {
        'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6',
        'Cookie' : 'BAIDUID=0062E94C2415A10D4A98C245AB0DCDB6:FG=1; BIDUPSID=0062E94C2415A10D4A98C245AB0DCDB6; PSTM=1476948431; PANWEB=1; bdshare_firstime=1478590959542; MCITY=-%3A; plus_cv=1::m:317d05a4; BDUSS=pBdjM1UFhTTH5kWmt0bzljb1BKcXNueGh2QUhrY2V2Vnk3UUlUVGNUUzliWGRZSVFBQUFBJCQAAAAAAAAAAAEAAAD4KMoI0KFMufnmwwAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAL3gT1i94E9Yc0; STOKEN=b75cfe6434a58f539c5203c004b80ab9883ee188c5b7cf5aa1a36bcd93a56441; SCRC=f46b2515666d3cf89a0aa578518fedf2; Hm_lvt_7a3960b6f067eb0085b7f96ff5e660b0=1481366129,1481629827,1481629840,1481629890; Hm_lpvt_7a3960b6f067eb0085b7f96ff5e660b0=1481633287; PSINO=3; H_PS_PSSID=1458_21421_21109_20593_21553_21408; PANPSC=2217017079170340720%3a0JkSUlxv8cVgObIo8FKEazAD4xI%2fb9r71xvRpgWaXhW2nqu%2f%2fiFUIj9hnwPONS7CfPb0JMZPTIz6Vzt6IJq7wb%2bz6U57xng7Vb5kimJikYQ%2bMIHUP9XFjCpOBrl9L%2fv6rGzifZv8N3pta40M9FeS7LHQG6qeixv0oOwnhPM9ZQ3XRwte8B0xUscsQW%2frTNKdec1jWKqTu%2flAbWykLXHYjsHr6br6XgqudzGMsemg9Mk%3d',
        'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36'
    }
    payload = {'channel': 'chunlei', 'web': '1', 'app_id': '250528', 'bdstoken': 'f1570965c3379608127c381148744e0e', 'logid': 'MTQ4MTYzNTkyOTA4NDAuMTY2Nzk3MTg3MDQxOTMwMjU=', 'clienttype': '0'}
    postdata = {
    'method' : 'query_magnetinfo',
    'app_id' : '250528',
    'source_url' : urlAddr,
    'save_path' : '/',
    'type' : '4'
    }
    r = requests.post(url='http://pan.baidu.com/rest/2.0/services/cloud_dl',params=payload,data = postdata,headers = header,proxies=proxies, verify=False,timeout=60)
def separate_str(addr):
    addrs =  addr.split("*")
    for a in addrs:
        if a:
            do_post(a)
if __name__ == '__main__':
    conn = sqlite3.connect('D:\\python\\db\\test.db')
    c = conn.cursor()
    #将喜欢的图片保存到指定文件夹后,读取图片的名称及就是编码,根据编号在数据库将下载地址找出来
    os.chdir(r'D:\IMG\like')
    for file_name in glob.glob("*.jpg"):
        cur = c.execute("select No,adrr from Aadrr where No = ?",(file_name.split('.')[0],))
        for row in cur:
            print('No = ', row[0])
            #print("地址", row[1])'
            print("将地址分割：\n")
            separate_str(row[1])
    conn.close()
#解析返回的数据
