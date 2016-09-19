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
    with open(file_url,'r') as f1:
        flists=f1.readlines()
        data=tuple([flist.strip() for flist in flists])
        return data

def get_token():
    s=requests.session()
    r=s.get('http://vip.jd.com/bean/25648761.html')
    cer=re.compile('pageConfig.token="(.*)"')
    token=cer.findall(r.text)[0]
    print('token='+token)
    return token

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

def post_page(cookie,password):
    global token,itemId
    headers={
    'Accept':'*/*',
    'Accept-Encoding':'gzip, deflate',
    'Accept-Language':'zh-CN,zh;q=0.8',
    'Connection':'keep-alive',
    'Origin':'http://vip.jd.com',
    'X-Requested-With':'XMLHttpRequest',
    'Cookie':cookie,
    'Host':'vip.jd.com',
    'Content-Type':'application/x-www-form-urlencoded',
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2743.116 Safari/537.36'
    }
    s=requests.session()
    s.headers=headers
    data='itemId={}&password={}&token={}'.format(itemId,password,token)
    try:
        r=s.post('http://vip.jd.com/bean/exchangeCoupon.html',data=data,timeout=1)
        if '提交错误' in r.text:
            token=get_token()
            return post_page(cookie,password)
    except:
        return post_page(cookie,password)
    else:
        print(r.text)




#模式1：对单个用户进行get操作
def one_get():
    n=int(input('请选择第n个用户进行操作：'))
    cookie=cookies[n-1]
    get_page(url,cookie)

#模式11：对单个用户进行post操作
def one_post():
    n=int(input('请选择第n个用户进行操作：'))
    cookie=cookies[n-1]
    password=passwords[n-1]
    post_page(cookie,password)

#模式2：对所有用户进行get操作
def all_get():
    for cookie in cookies:
        t=threading.Thread(target=get_page,args=(url,cookie))
        t.start()

#模式12：对所有用户进行post操作
def all_post():
    for i in range(len(passwords)):
        cookie,password=cookies[i],passwords[i]
        t=threading.Thread(target=post_page,args=(cookie,password))
        t.start()

#模式3：对单个用户进行定时get操作
def time_one_get():
    n=int(input('请选择第n个用户进行操作：'))
    cookie=cookies[n-1]
    timer()
    get_page(url,cookie)

#模式13：对单个用户进行定时post操作
def time_one_post():
    n=int(input('请选择第n个用户进行操作：'))
    cookie=cookies[n-1]
    password=passwords[n-1]
    timer()
    post_page(cookie,password)


#模式4：对所有用户进行定时get操作
def time_all_get():
    timer()
    all_get()

#模式14：对所有用户进行定时post操作
def time_all_post():
    timer()
    all_post()

#模式5：对单个用户进行循环get操作
def loop_one_get():
    n=int(input('请选择第n个用户进行操作：'))
    loop_times=int(input('请输入循环次数：'))
    cookie=cookies[n-1]
    for i in range(loop_times):
        t=threading.Thread(target=get_page,args=(url,cookie))
        t.start()
        #time.sleep(3)

#模式15：对单个用户进行循环post操作
def loop_one_post():
    n=int(input('请选择第n个用户进行操作：'))
    loop_times=int(input('请输入循环次数：'))
    cookie=cookies[n-1]
    password=passwords[n-1]
    for i in range(loop_times):
        t=threading.Thread(target=post_page,args=(cookie,password))
        t.start()

#模式6：对所有用户进行循环get操作
def loop_all_get():
    loop_times=int(input('请输入循环次数：'))
    for i in range(loop_times):
        all_get()
        #time.sleep(1)

#模式16：对所有用户进行循环post操作
def loop_all_post():
    loop_times=int(input('请输入循环次数：'))
    for i in range(loop_times):
        all_post()
        time.sleep(5)

#模式7：对单个用户进行定时循环get操作
def loop_time_one_get():
    n=int(input('请选择第n个用户进行操作：'))
    loop_times=int(input('请输入循环次数：'))
    cookie=cookies[n-1]
    timer()
    for i in range(loop_times):
        t=threading.Thread(target=get_page,args=(url,cookie))
        t.start()

#模式17：对单个用户进行定时循环post操作
def loop_time_one_post():
    n=int(input('请选择第n个用户进行操作：'))
    loop_times=int(input('请输入循环次数：'))
    cookie=cookies[n-1]
    password=passwords[n-1]
    timer()
    for i in range(loop_times):
        t=threading.Thread(target=post_page,args=(cookie,password))
        t.start()

#模式8：对所有用户进行定时循环get操作
def loop_time_all_get():
    loop_times=int(input('请输入循环次数：'))
    timer()
    for i in range(loop_times):
        all_get()

#模式18：对所有用户进行定时循环post操作
def loop_time_all_post():
    loop_times=int(input('请输入循环次数：'))
    timer()
    for i in range(loop_times):
        all_post()

#模式19：对单个用户永久循环post
def loop_forever_one_post():
    n=int(input('请选择第n个用户进行操作：'))
    cookie=cookies[n-1]
    password=passwords[n-1]
    while True:
        post_page(cookie,password)
        time.sleep(5)

operator={1:one_get,2:all_get,3:time_one_get,4:time_all_get,5:loop_one_get,6:loop_all_get,7:loop_time_one_get,8:loop_time_all_get,11:one_post,12:all_post,13:time_one_post,14:time_all_post,15:loop_one_post,16:loop_all_post,17:loop_time_one_post,18:loop_time_all_post,19:loop_forever_one_post}

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
print('*=========================================*')
print('*            (11)对单个用户post           *')
print('*            (12)对所有用户post           *')
print('*            (13)对单个用户定时post       *')
print('*            (14)对所有用户定时post       *')
print('*            (15)对单个用户循环post       *')
print('*            (16)对所有用户循环post       *')
print('*            (17)对单个用户定时循环post   *')
print('*            (18)对所有用户定时循环post   *')
print('*            (19)对单个用户永久循环post   *')
print('*            (0)退出                     *')
print('*=========================================*')

y=int(input('请选择模式（y）：'))
if y in operator.keys():
    urls=get_userdata('C:\\Users\肥皂\Desktop\\url.txt')
    cookies=get_userdata('C:\\Users\肥皂\Desktop\\ck.txt')
    passwords=get_userdata('C:\\Users\肥皂\Desktop\\password.txt')
    if y<10:
        x=int(input('请选择第x个url：'))
        url=urls[x-1]
    else:
        passwords=get_userdata('C:\\Users\肥皂\Desktop\\password.txt')
        for password in passwords:
            if '?' in password:
                password.replace(' ','%3F')
    token=get_token()
    itemId='25649604'
    f(y)
elif y==0:
    exit()
else:
    print('模式输入错误！')