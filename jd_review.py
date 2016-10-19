import requests
import json
import mysql.connector

class reviewer(object):
    def __init__(self):
        self.score_dict={1:'差评',2:'中评',3:'好评'}

    def get_referenceId(self):
        self.product_id=input('请输入要抓取的京东商品ID：')

    def save_data(self):
        self.conn=mysql.connector.connect(user='root',password='')
        self.cursor=self.conn.cursor()
        self.cursor.execute('create database if not exists jd')
        self.conn.connect(database='jd')
        self.connnect()

    def connnect(self):
        try:
            self.cursor.execute('create table %s (id varchar(200) primary key,nickname varchar(20),content varchar(500),score char(1))' %('goods_'+self.product_id))
        except mysql.connector.Error as e:
            flag=input('您已爬取过该商品的评价，您确定要重新爬取吗？y/n:')
            if flag=='y':
                self.cursor.execute('drop table %s' %('goods_'+self.product_id))
                return self.connnect()
            else:
                print('程序退出')
                exit()
        except Exception as e:
            print(e)
            exit(-1)

    def find_review(self,score,max_page=100):
        page=0
        page_data=''
        while True:
            url='https://sclub.jd.com/comment/productPageComments.action?productId={}&score={}&sortType=3&page={}&pageSize=10'.format(self.product_id,score,page)
            r=requests.get(url)
            if page_data==r.text:
                return page
            page_data=r.text
            data=json.loads(page_data)
            if len(data['comments']) and page<max_page:
                print('\n\nsore=',self.score_dict[score],'\tpage=',page)
                for review in data['comments']:
                    if review['referenceId']==self.product_id:
                        self.count+=1
                        do='insert into goods_'+self.product_id+' (id,nickname,content,score) values(%s,%s,%s,%s)'
                        try:
                            self.cursor.execute(do,(str(self.count),review['nickname'],review['content'],review['score']))
                            self.conn.commit()
                        except Exception as e:
                            print(e)
                            pass
                        print(self.count,review['nickname'],review['content'],review['score'])
                page+=1
            else:
                return page

    def run_review(self):
        self.get_referenceId()
        self.save_data()
        self.count=0
        max_page=self.find_review(score=1)
        max_page+=self.find_review(score=2)
        self.find_review(score=3,max_page=max_page)
        self.conn.close()