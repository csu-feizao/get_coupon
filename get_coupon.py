import requests
import time,threading
import re

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

urls=get_userdata('urls.txt')
cookies=get_userdata('cookies.txt')
s=requests.session()
x=int(input('请选择第x个url：'))


def get_page(cookie):
    headers={
    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Encoding':'gzip, deflate, sdch',
    'Accept-Language':'zh-CN,zh;q=0.8',
    'Connection':'keep-alive',
    'Cookie':cookie,
    'Host':'coupon.jd.com',
    'Cache-Control':'max-age=0',
    'Upgrade-Insecure-Requests':'1',
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'
    }
    url=urls[x-1]
    r=s.get(url,headers=headers)
#    print(r.text)
    cer=re.compile('<h1 class="ctxt02"><s class="icon-redbag"></s>(.*)~</h1>',flags=0)
    strlist=cer.findall(r.text)
    print(strlist[0])


#模式1：对单个用户进行get操作
def one_get():
    n=int(input('请选择第n个用户进行操作：'))
    cookie=cookies[n-1]
    t=threading.Thread(target=get_page(cookie))
    t.start()

#模式2：对所有用户进行get操作
def all_get():
    for cookie in cookies:
        t=threading.Thread(target=get_page(cookie))
        t.start()

#模式3：对单个用户进行定时get操作
def time_one_get():
    n=int(input('请选择第n个用户进行操作：'))
    target_time=input('请输入开始时间（如00:00:00）：')
    run=True
    while run:
        if time.ctime()[11:19]==target_time:
            start=time.clock()
            cookie=cookies[n-1]
            t=threading.Thread(target=get_page(cookie))
            t.start()
            end=time.clock()
            print('共用时%s秒' %(end-start))
            run=False

#模式4：对所有用户进行定时get操作
def time_all_get():
    target_time=input('请输入开始时间（如00:00:00）：')
    run=True
    while run:
        if time.ctime()[11:19]==target_time:
            start=time.clock()
            all_get()
            end=time.clock()
            print('共用时%s秒' %(end-start))
            run=False

#模式5：对单个用户进行循环get操作
def loop_one_get():
    n=int(input('请选择第n个用户进行操作：'))
    loop_times=int(input('请输入循环次数：'))
    start=time.clock()
    for i in range(loop_times):
        cookie=cookies[n-1]
        t=threading.Thread(target=get_page(cookie))
        t.start()
    end=time.clock()
    print('共用时%s秒' %(end-start))

#模式6：对所有用户进行循环get操作
def loop_all_get():
    loop_times=int(input('请输入循环次数：'))
    start=time.clock()
    for i in range(loop_times):
        all_get()
    end=time.clock()
    print('共用时%s秒' %(end-start))

#模式7：对单个用户进行定时循环get操作
def loop_time_one_get():
    n=int(input('请选择第n个用户进行操作：'))
    target_time=input('请输入开始时间（如00:00:00）：')
    loop_times=int(input('请输入循环次数：'))
    run=True
    while run:
        if time.ctime()[11:19]==target_time:
            start=time.clock()
            for i in range(loop_times):
                cookie=cookies[n-1]
                t=threading.Thread(target=get_page(cookie))
                t.start()
            end=time.clock()
            print('共用时%s秒' %(end-start))
            run=False

#模式8：对所有用户进行定时循环get操作
def loop_time_all_get():
    target_time=input('请输入开始时间（如00:00:00）：')
    loop_times=int(input('请输入循环次数：'))
    run=True
    while run:
        if time.ctime()[11:19]==target_time:
            start=time.clock()
            for i in range(loop_times):
                all_get()
            end=time.clock()
            print('共用时%s秒' %(end-start))
            run=False


operator={1:one_get,2:all_get,3:time_one_get,4:time_all_get,5:loop_one_get,6:loop_all_get,7:loop_time_one_get,8:loop_time_all_get}

def f(n):
    operator.get(n)()
    print('完成')

print('*=============请选择操作模式==============*')
print('*            (1)对单个用户get             *')
print('*            (2)对所有用户get             *')
print('*            (3)对单个用户定时get         *')
print('*            (4)对所有用户定时get         *')
print('*            (5)对单个用户循环get         *')
print('*            (6)对所有用户循环get         *')
print('*            (7)对单个用户定时循环get     *')
print('*            (8)对所有用户定时循环get     *')
print('*=========================================*')

y=int(input('请选择模式（y）：'))
if y in operator.keys():
    f(y)
else:
    print('模式输入错误！')