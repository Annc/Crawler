#coding:utf8
import sqlite3
import glob
import os
import requests
from lxml import html
import json
import time
requests.packages.urllib3.disable_warnings()
proxies = {
    'http' : "http://127.0.0.1:8888",
    'https' : "https://127.0.0.1:8888",
    #'http': "socks5://127.0.0.1:1080",
    #'https': "socks5://127.0.0.1:1080"
}
def do_post_two(urlAddr,num):
    now_time = int(time.time() * 1000)
    s = '1'
    if num > 1:
        for i in range(2,num):
            s = s + ',' + str(i)
    header = {
        'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6',
        'Cookie' : 'BAIDUID=0062E94C2415A10D4A98C245AB0DCDB6:FG=1; BIDUPSID=0062E94C2415A10D4A98C245AB0DCDB6; PSTM=1476948431; PANWEB=1; bdshare_firstime=1478590959542; MCITY=-%3A; plus_cv=1::m:317d05a4; PSINO=3; H_PS_PSSID=1458_21421_21109_20593_21553_21408; BDUSS=WZwelZESENweWlFNFFlSVhpVllPQVV4TFNaSmdBZX5-a0Ftb1g4bjFYUTBJWHRZSVFBQUFBJCQAAAAAAAAAAAEAAABL5twwd290b25tYW4AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAADSUU1g0lFNYO; STOKEN=cfb38ac4ed483e0dacb2b22d03b1a53523243214b4469e6b958055e19ca05631; SCRC=83c61c55f2bde03134765ac3de0aa25e; cflag=15%3A3; recommendTime=guanjia2016-12-15%2018%3A55; Hm_lvt_7a3960b6f067eb0085b7f96ff5e660b0=1481629890,1481698272,1481698327,1481869088; Hm_lpvt_7a3960b6f067eb0085b7f96ff5e660b0=1481872577; PANPSC=4153304652178177547%3AEFB88jicTNLjWtevpTwoyu8QioVhG8m3AlMuQaS5p19Ku8WyLCLL4a1wwlQMCvHkxwoAmFE3cTAACjQwe5HWyAMfViViY21lb4g8ZGlzcStuWt7N7jFSoGVWcHP9mn3MPjCB1D%2FVxYyaB5R8hpvpEDWPC7NKcJhViVE530gHCys%3D',
        'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36'
    }
    payload = {'channel': 'chunlei', 'web': '1', 'app_id': '250528', 'bdstoken': 'fb76b7b49a38d641a6039c30b3ceddc5', 'logid': 'MTQ4MTg3Mjg4NzE0NTAuOTk5MjAzODE2Mzc0NTQwNQ==', 'clienttype': '0'}
    postdata = {
    'method' : 'add_task',
    'app_id' : '250528',
    'file_sha1' : '',
    'save_path' : '/test_down/',
    'selected_idx' : s,
    'task_from' : '1',
    't' : now_time,
    'source_url' : urlAddr,
    'type' : '4'
    }
    r = requests.post(url='http://pan.baidu.com/rest/2.0/services/cloud_dl',params=payload,data = postdata,headers = header,proxies=proxies, verify=False,timeout=60)
    return r

def do_post(urlAddr):
    #cookie是变化的
    header = {
        'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6',
        'Cookie' : 'BAIDUID=0062E94C2415A10D4A98C245AB0DCDB6:FG=1; BIDUPSID=0062E94C2415A10D4A98C245AB0DCDB6; PSTM=1476948431; PANWEB=1; bdshare_firstime=1478590959542; MCITY=-%3A; plus_cv=1::m:317d05a4; PSINO=3; H_PS_PSSID=1458_21421_21109_20593_21553_21408; BDUSS=WZwelZESENweWlFNFFlSVhpVllPQVV4TFNaSmdBZX5-a0Ftb1g4bjFYUTBJWHRZSVFBQUFBJCQAAAAAAAAAAAEAAABL5twwd290b25tYW4AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAADSUU1g0lFNYO; STOKEN=cfb38ac4ed483e0dacb2b22d03b1a53523243214b4469e6b958055e19ca05631; SCRC=83c61c55f2bde03134765ac3de0aa25e; cflag=15%3A3; recommendTime=guanjia2016-12-15%2018%3A55; Hm_lvt_7a3960b6f067eb0085b7f96ff5e660b0=1481629890,1481698272,1481698327,1481869088; Hm_lpvt_7a3960b6f067eb0085b7f96ff5e660b0=1481872577; PANPSC=4153304652178177547%3AEFB88jicTNLjWtevpTwoyu8QioVhG8m3AlMuQaS5p19Ku8WyLCLL4a1wwlQMCvHkxwoAmFE3cTAACjQwe5HWyAMfViViY21lb4g8ZGlzcStuWt7N7jFSoGVWcHP9mn3MPjCB1D%2FVxYyaB5R8hpvpEDWPC7NKcJhViVE530gHCys%3D',
        'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36'
    }
    payload = {'channel': 'chunlei', 'web': '1', 'app_id': '250528', 'bdstoken': 'fb76b7b49a38d641a6039c30b3ceddc5', 'logid': 'MTQ4MTg3Mjg4NzE0NTAuOTk5MjAzODE2Mzc0NTQwNQ==', 'clienttype': '0'}
    postdata = {
    'method' : 'query_magnetinfo',
    'app_id' : '250528',
    'source_url' : urlAddr,
    'save_path' : '/test_down/',
    'type' : '4'
    }
    r = requests.post(url='http://pan.baidu.com/rest/2.0/services/cloud_dl',params=payload,data = postdata,headers = header,proxies=proxies, verify=False,timeout=60)
    return r

def separate_str(addr):
    addrs =  addr.split("*")
    for a in addrs:
        if a:
            time.sleep(20)
            result = do_post(a)
            if result.status_code == 200:
                r_json = json.loads(result.text)
                time.sleep(30)
                add_task_result = do_post_two(a,r_json['total'])
                if add_task_result.status_code == 200:
                    print("成功: " + a + "\n")
                    break
                #print(r_json)
                #print('json的key:\n')
                #print(r_json.keys())
if __name__ == '__main__':
    conn = sqlite3.connect('D:\\python\\db\\test.db')
    c = conn.cursor()
    #将喜欢的图片保存到指定文件夹后,读取图片的名称及就是编码,根据编号在数据库将下载地址找出来
    os.chdir(r'D:\IMG\like')
    for file_name in glob.glob("*.jpg"):
        cur = c.execute("select No,adrr from Aadrr where No = ?",(file_name.split('.')[0],))
        for row in cur:
            #print('No = ', row[0])
            separate_str(row[1])
    conn.close()
#解析返回的数据
