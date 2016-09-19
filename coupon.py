import requests
import time,threading
import re,ntplib

class Time(object):
    def get_ntptime(self):
        client=ntplib.NTPClient()
        try:
            response=client.request('202.108.6.95',timeout=1)
        except ntplib.NTPException:
            print('校正超时，重新校正...')
            return self.get_ntptime()
        else:
            my_timestamp=response.tx_time
            print('校正时间：',my_timestamp)
            return  my_timestamp

    def timer(self):
        print('当前时间：',time.strftime('%Y-%m-%d %H;%M:%S',time.localtime(self.get_ntptime())))
        target_time=input('请输入目标时间（如00:00:00）：')
        date=time.strftime('%Y-%m-%d',time.localtime(time.time()))
        target_stamp=time.mktime(time.strptime((date+' '+target_time),'%Y-%m-%d %H:%M:%S'))
        print('目标时间：',time.strftime('%Y-%m-%d %H;%M:%S',time.localtime(target_stamp)))
        print('定时等待中...')
        my_timestamp=self.get_ntptime()
        i=0
        while my_timestamp<target_stamp:
            my_timestamp+=1
            i+=1
            if i%5==0:
                my_timestamp=self.get_ntptime()
            time.sleep(1)


class MyInfo(object):
    def get_userdata(self,file_url):
        with open(file_url,'r') as f1:
            flists=f1.readlines()
            data=tuple([flist.strip() for flist in flists])
            return data

    def set_urls(self,urls):
        self.urls=self.get_userdata(urls)

    def set_cookies(self,cookies_url):
        self.cookies=self.get_userdata(cookies_url)

    def set_headers(self,cookie):
        self.headers={
                        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                        'Accept-Encoding':'gzip, deflate, sdch',
                        'Accept-Language':'zh-CN,zh;q=0.8',
                        'Connection':'keep-alive',
                        'Cookie':cookie,
                        'Cache-Control':'max-age=0',
                        'Upgrade-Insecure-Requests':'1',
                        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2743.116 Safari/537.36'
                        }


class GetCoupon(MyInfo):
    def get_page(self,m):
        s=requests.session()
        s.headers=self.headers
        try:
            r=s.get(self.urls[m-1],timeout=1)
        except requests.TooManyRedirects:
            print('cookie失效，原因不明（可能是半白号，访问过快触发京东保护机制），请重新提取cookie')
        except requests.ConnectTimeout:
            print('超时重试中,若依然如此请检查网络')
            return self.get_page(m)
        else:
            cer=re.compile('<h1 class="ctxt02"><s class="icon-redbag"></s>(.*)</h1>',flags=0)
            strlist=cer.findall(r.text)
            if not strlist:
                print('未知错误')
            else:
                print(strlist[0])

    def one_get(self,n,m):
        self.set_headers(self.cookies[n-1])
        self.get_page(m)

    def loop_one_get(self,n,m,loop_times):
        self.set_headers(self.cookies[n-1])
        for i in range(loop_times):
            t=threading.Thread(target=self.get_page,args=(m,))
            t.start()

    def all_get(self,m):
        for cookie in self.cookies:
            self.set_headers(cookie)
            t=threading.Thread(target=self.get_page,args=(m,))
            t.start()

    def loop_all_get(self,m,loop_times):
        for i in range(loop_times):
            self.all_get(m)


class PostCoupon(MyInfo):
    def set_passwords(self,passwords_url):
        self.passwords=self.get_userdata(passwords_url)

    def set_itemId(self,itemId):
        self.itemId=itemId

    def get_token(self):
        s=requests.session()
        r=s.get('http://vip.jd.com/bean/{}.html'.format(self.itemId))
        cer=re.compile('pageConfig.token="(.*)"')
        self.token=cer.findall(r.text)[0]
        print('token='+self.token)

    def post_page(self,password):
        s=requests.session()
        s.headers=self.headers
        self.data='itemId={}&password={}&token={}'.format(self.itemId,password,self.token)
        try:
            r=s.post('http://vip.jd.com/bean/exchangeCoupon.html',data=self.data,timeout=1)
            if '提交错误' in r.text:
                self.get_token()
                return self.post_page(password)
        except:
            return self.post_page(password)
        else:
            print(r.text)

    def one_post(self,n,m):
        self.set_headers(self.cookies[n-1])
        self.headers['Content-Type']='application/x-www-form-urlencoded'
        self.post_page(m[n-1])

    def loop_one_post(self,n,m,loop_times):
        self.set_headers(self.cookies[n-1])
        self.headers['Content-Type']='application/x-www-form-urlencoded'
        for i in range(loop_times):
            t=threading.Thread(target=self.post_page,args=(m[n-1],))
            t.start()

    def all_post(self,m):
        for i in range(len(self.passwords)):
            password=m[i]
            self.set_headers(self.cookies[i])
            self.headers['Content-Type']='application/x-www-form-urlencoded'
            t=threading.Thread(target=self.post_page,args=(password,))
            t.start()

    def loop_all_post(self,m,loop_times):
        for i in range(loop_times):
            self.all_post(m)


class Coupon(Time,GetCoupon,PostCoupon):
    def __init__(self):
        print('*===============请选择操作模式================*')
        print('*          (1)单个用户                       *')
        print('*          (2)所有用户                       *')
        print('*          (3)单个用户 and 循环              *')
        print('*          (4)所有用户 and 循环              *')
        print('*          (5)单个用户 and 定时              *')
        print('*          (6)所有用户 and 定时              *')
        print('*          (7)单个用户 and 定时 and 循环     *')
        print('*          (8)所有用户 and 定时 and 循环     *')
        self.set_urls('C:\\Users\肥皂\Desktop\\url.txt')
        self.set_cookies('C:\\Users\肥皂\Desktop\\ck.txt')

    def run(self):
        name=input('请选择（1）get或（2）post：').strip()
        if name=='1':
            name='get'
            m=int(input('请选择第m个url：'))
        elif name=='2':
            name='post'
            itemId=input('请输入itemId(参考http://vip.jd.com/bean/(itemId).html)：')
            self.set_itemId(itemId)
            self.get_token()
            self.set_passwords('C:\\Users\肥皂\Desktop\\password.txt')
            m=self.passwords
        else:
            print('输入错误，请重新输入！')
            return self.run()
        y=int(input('请选择模式（y）：'))
        if y==1:
            n=int(input('请选择第n个用户操作：'))
            eval('self.one_{}'.format(name))(n,m)
        elif y==2:
            eval('self.all_{}'.format(name))(m)
        elif y==3:
            n=int(input('请选择第n个用户操作：'))
            loop_times=int(input('请输入循环次数：'))
            eval('self.loop_one_{}'.format(name))(n,m,loop_times)
        elif y==4:
            loop_times=int(input('请输入循环次数：'))
            eval('self.loop_all_{}'.format(name))(m,loop_times)
        elif y==5:
            n=int(input('请选择第n个用户操作：'))
            self.timer()
            eval('self.one_{}'.format(name))(n,m)
        elif y==6:
            self.timer()
            eval('self.all_{}'.format(name))(m)
        elif y==7:
            n=int(input('请选择第n个用户操作：'))
            loop_times=int(input('请输入循环次数：'))
            self.timer()
            eval('self.loop_one_{}'.format(name))(n,m,loop_times)
        elif y==8:
            loop_times=int(input('请输入循环次数：'))
            self.timer()
            eval('self.loop_all_{}'.format(name))(m,loop_times)
        else:
            print('模式输入错误，请重新输入！')
            return self.run()

if __name__=='__main__':
    c=Coupon()
    c.run()

