import ntplib,time

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