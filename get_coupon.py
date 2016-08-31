import requests
import time,threading
import re,ntplib

def get_ntptime():
    client=ntplib.NTPClient()
    try:
        response=client.request('202.108.6.95',timeout=1)
    except ntplib.NTPException:
        print('校正超时，重新校正...')
        return get_ntptime()
    else:
        my_timestamp=response.tx_time
        print('校正时间：',my_timestamp)
        return  my_timestamp

def timer():
    print('当前时间：',time.strftime('%Y-%m-%d %H;%M:%S',time.localtime(get_ntptime())))
    target_time=input('请输入目标时间（如00:00:00）：')
    date=time.strftime('%Y-%m-%d',time.localtime(time.time()))
    target_stamp=time.mktime(time.strptime((date+' '+target_time),'%Y-%m-%d %H:%M:%S'))
    print('目标时间：',time.strftime('%Y-%m-%d %H;%M:%S',time.localtime(target_stamp)))
    print('定时等待中...')
    my_timestamp=get_ntptime()
    i=0
    while my_timestamp<target_stamp:
        my_timestamp+=1
        i+=1
        if i%5==0:
            my_timestamp=get_ntptime()
        time.sleep(1)

def get_userdata(file_url):
    data=[]
    with open(file_url,'r') as f1:
        flists=f1.readlines()
        for flist in flists:
            if flist[-1]=='\n':
                flist=flist[0:-1]
            data.append(flist)
        data=tuple(data)
        return data

def get_page(url,cookie):
    headers={
    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Encoding':'gzip, deflate, sdch',
    'Accept-Language':'zh-CN,zh;q=0.8',
    'Connection':'keep-alive',
    'Cookie':cookie,
    'Host':'active.coupon.jd.com',
    'Cache-Control':'max-age=0',
    'Upgrade-Insecure-Requests':'1',
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2743.116 Safari/537.36'
    }
    s=requests.session()
    s.headers=headers
    try:
        r=s.get(url)
        #print(r.url,r.status_code,r.history)
    except requests.TooManyRedirects:
        print('cookie失效，原因不明（可能是访问过快触发京东保护机制，使用fiddler狂R也会出现该问题，故非代码原因），请重新提取cookie')
    else:
        cer=re.compile('<h1 class="ctxt02"><s class="icon-redbag"></s>(.*)</h1>',flags=0)
        strlist=cer.findall(r.text)
        if not strlist:
            print('未知错误')
        else:
            print(strlist[0])


#模式1：对单个用户进行get操作
def one_get():
    n=int(input('请选择第n个用户进行操作：'))
    cookie=cookies[n-1]
    get_page(url,cookie)

#模式2：对所有用户进行get操作
def all_get():
    for cookie in cookies:
        t=threading.Thread(target=get_page,args=(url,cookie))
        t.start()

#模式3：对单个用户进行定时get操作
def time_one_get():
    n=int(input('请选择第n个用户进行操作：'))
    timer()
    cookie=cookies[n-1]
    get_page(url,cookie)

#模式4：对所有用户进行定时get操作
def time_all_get():
    timer()
    all_get()

#模式5：对单个用户进行循环get操作
def loop_one_get():
    n=int(input('请选择第n个用户进行操作：'))
    loop_times=int(input('请输入循环次数：'))
    for i in range(loop_times):
        cookie=cookies[n-1]
        t=threading.Thread(target=get_page,args=(url,cookie))
        t.start()

#模式6：对所有用户进行循环get操作
def loop_all_get():
    loop_times=int(input('请输入循环次数：'))
    for i in range(loop_times):
        all_get()

#模式7：对单个用户进行定时循环get操作
def loop_time_one_get():
    n=int(input('请选择第n个用户进行操作：'))
    loop_times=int(input('请输入循环次数：'))
    timer()
    for i in range(loop_times):
        cookie=cookies[n-1]
        t=threading.Thread(target=get_page,args=(url,cookie))
        t.start()

#模式8：对所有用户进行定时循环get操作
def loop_time_all_get():
    loop_times=int(input('请输入循环次数：'))
    timer()
    for i in range(loop_times):
        all_get()

operator={1:one_get,2:all_get,3:time_one_get,4:time_all_get,5:loop_one_get,6:loop_all_get,7:loop_time_one_get,8:loop_time_all_get}

def f(n):
    operator.get(n)()

print('*=============请选择操作模式==============*')
print('*            (1)对单个用户get             *')
print('*            (2)对所有用户get             *')
print('*            (3)对单个用户定时get         *')
print('*            (4)对所有用户定时get         *')
print('*            (5)对单个用户循环get         *')
print('*            (6)对所有用户循环get         *')
print('*            (7)对单个用户定时循环get     *')
print('*            (8)对所有用户定时循环get     *')
print('*            (0)退出                     *')
print('*=========================================*')

y=int(input('请选择模式（y）：'))
if y in operator.keys():
    urls=get_userdata('C:\\Users\肥皂\Desktop\\url.txt')
    cookies=get_userdata('C:\\Users\肥皂\Desktop\\ck.txt')
    x=int(input('请选择第x个url：'))
    url=urls[x-1]
    f(y)
elif y==0:
    exit()
else:
    print('模式输入错误！')