import requests
import json
import mysql.connector

class reviewer(object):
    def __init__(self):
        self.flag='0'
        self.score_dict={1:'negative',2:'neutral',3:'positive'}

    def connect_mysql(self):
        self.conn=mysql.connector.connect(user='root',password='')
        self.cursor=self.conn.cursor()
        self.cursor.execute('create database if not exists jd')
        self.conn.connect(database='jd')
        self.create_table()

    def create_table(self):
        try:
            self.cursor.execute('create table %s (id varchar(200) primary key,nickname varchar(20),content varchar(500),score char(1),classify varchar(20))' %('goods_'+self.product_id))
        except mysql.connector.Error as e:
            self.flag=input('您已爬取过该商品的评价，您确定要重新爬取吗？y/n:')
            if self.flag=='y':
                self.cursor.execute('drop table %s' %('goods_'+self.product_id))
                return self.create_table()
            elif self.flag=='n':
                return
            else:
                print('输入错误！')
                return self.create_table()
        except Exception as e:
            print(e)
            exit(-1)

    def find_review(self,score,max_page=20):
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
                        do='insert into goods_'+self.product_id+' (id,nickname,content,score,classify) values(%s,%s,%s,%s,%s)'
                        try:
                            self.cursor.execute(do,(str(self.count),review['nickname'],review['content'],review['score'],self.score_dict[score]))
                            self.conn.commit()
                        except Exception as e:
                            print(e)
                        print(self.count,review['nickname'],review['content'],review['score'])
                page+=1
            else:
                return page

    def run_review(self):
        self.product_id=input('请输入要查询的商品ID：')
        self.connect_mysql()
        if self.flag=='0' or self.flag=='y':
            self.count=0
            self.find_review(score=1)
            self.find_review(score=2)
            self.find_review(score=3)
        self.conn.close()