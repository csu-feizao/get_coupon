import requests,json,re
class Stock(object):
    def __init__(self):
        self.province_dict={value:key for key,value in {
            1:'北京',2:'上海',3:'天津',4:'重庆',5:'河北',6:'山西',7:'河南',8:'辽宁',9:'吉林',10:'黑龙江',
            11:'内蒙古',12:'江苏',13:'山东',14:'安徽',15:'浙江',16:'福建',17:'湖北',18:'湖南',19:'广东',20:'广西',
            21:'江西',22:'四川',23:'海南',24:'贵州',25:'云南',26:'西藏',27:'陕西',28:'甘肃',29:'青海',30:'宁夏',
            31:'新疆',32:'台湾'
        }.items()}
        self.price_dict={
            'PC端':'https://p.3.cn/prices/get?type=1&skuid=J_{}',
            'APP端':'https://pm.3.cn/prices/mgets?origin=2&skuIds={}',
            '微信端':'https://pe.3.cn/prices/mgets?origin=5&skuids={}',
            'QQ端':'https://pe.3.cn/prices/mgets?origin=4&skuids={}'
        }
        self.set_skuId()

    def set_skuId(self):
        self.skuId=input('请输入商品ID：')
        r=requests.get('http://item.jd.com/{}.html'.format(self.skuId)).text
        cer=re.compile('<title>(.*)</title>',flags=0)
        self.skuName=cer.findall(r)
        if not self.skuName:
            print('您输入的商品ID有误！')
            return self.set_skuId()
        else:
            print(self.skuName[0])

    def get_price(self):
        for key,value in self.price_dict.items():
            r=json.loads(requests.get(value.format(self.skuId)).text)[0]['p']
            print(key,r)


    def get_stock(self):
        provinceName=input('请输入要查询的省份(如湖南)：')
        if provinceName in self.province_dict.keys():
            r=json.loads(requests.get('https://c0.3.cn/stock?skuId={skuId}&cat=1316,1385,1408&area={province}_2805_2855'.format(skuId=self.skuId,province=str(self.province_dict[provinceName]))+'&extraParam={%22originid%22:%221%22}').text)
            print(r['stock']['area']['provinceName'],'：',r['stock']['StockStateName'])
        else:
            print('您的输入有误，请重新输入！')
            return self.get_stock()