import requests,time

def get_page(url,cookie):
    headers={
    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Encoding':'gzip, deflate, sdch',
    'Accept-Language':'zh-CN,zh;q=0.8',
    'Connection':'keep-alive',
    'Cookie':cookie,
    'Host':'h5.m.jd.com',
    'Cache-Control':'max-age=0',
    'Upgrade-Insecure-Requests':'1',
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2743.116 Safari/537.36'
    }
    s=requests.session()
    s.headers=headers
    try:
        r=s.get(url)
        print(r.text)
        #print(r.url,r.status_code,r.history)
    except requests.TooManyRedirects:
        print('cookie失效，原因不明（可能是访问过快触发京东保护机制，使用fiddler狂R也会出现该问题，故非代码原因），请重新提取cookie')



if __name__=='__main__':
    cookies=['abtest=20160323194724553_60; jdAddrId=; jdAddrName=; __utmmobile=0xeb89634461b673d0.1458733686583.1463671843758.1464275171076.448; __mjdv=androidapp|t_335139774|appshare|CopyURL; mt_xid=V2_52007VwATW1tQV1oZSh9sUWMCFFFaCwdGF0FMWBliAxQAQQtQXhtVTF1QbwAXBVsLWw5IeRpdBWAfE1tBWlNLH0oSXg1sARFiX2hRahtKH1wAYDMSVlw%3D; user-key=e328fc1a-c72b-453b-bfc3-b060da235479; unpl=V2_ZzNtbUJeQhZzXxMGfx4IVWJWEg0SXhEQJghBVCxOXFU0ChZYclRCFXIUR1xnGFsUZwEZXEBcQRFFCHZUehhdBGYFElhHZ3Mldgh2VnopXwRuBRpYQlFAE0U4QWRLGVgNYAIUWUNeQRUbSXZReB1bAmMDGlhyVnMQdwFPVXsbVAZXSHxcD1RCHHMAQ1R9Glo1ZwITXENWQhJ1DnZX; __jdv=209750407|baidu|-|organic|not set; TrackID=1P89q84f9P22gugvYFKHdwmtB7DECONF58OfE1B7mHZj5Q_VoKsqt-PYuMv-7ncPkXx8Nrz1uBIPU1YUWaCAIT88lDBAnr0RLMibB9MSFNiU; pinId=CsIGOo9O-PGq8_grK3BtOw; pin=%E5%88%BA%E7%8C%ACde%E6%82%B2%E6%AE%87; unick=%E5%88%BA%E7%8C%ACde%E6%82%B2%E6%AE%87; _tp=7ya0Bcdg4WVpXmgARKYeMp6%2BXGxhS6quknx1hdOZrnl6jPh9RtHpa8b%2Bvg4ty5G1; _pst=%E5%88%BA%E7%8C%ACde%E6%82%B2%E6%AE%87; ceshi3.com=mUtY19Fn3gWB7jpY3sV-aneSUB_z1mx0kQ1EsuTojcc; ipLocation=%u5317%u4EAC; areaId=1; ipLoc-djd=1-72-2799-0; cn=0; sid=c2dccf4bab8cef22b609afa038a3b604; USER_FLAG_CHECK=ac01d7c60ae5134bc23ca6c809f9d929; whwswswws=5HzYgyUHXzbc+tR6DaXbukPAxnL2GXYRKtvkIZBeLUBoRZn9wP0IWw%3D%3D; returnurl="http://h5.m.jd.com/active/3FEFWVbwgFD97sPwoF6hBnwJyUvr/index.html?coupon=250&win=true&sid=c2dccf4bab8cef22b609afa038a3b604"; thor=F5057CD1A558123EB9053AC0CCC4082DD4A0DB21F46A9C0D406334629638A7B1D9F503D928B473381F36AAD05D3E58E6759103F4C8505BD42B3BBCE6C1DC4FEAB9C677E4E4989370257BB7AF538E4B9A5D0BE6F2E698B871FC36E7FD6FED1CEDBF06621B7CD6CE4556A6187A40A364096E8B5DBCEA017FAF7E90FD11BEFA8C2D; __jda=122270672.2087941727.1458619796.1473321579.1473350464.480; __jdb=122270672.13.2087941727|480.1473350464; __jdc=122270672; __jdu=2087941727',
             'mobilev=html5; sid=8f1c8d088590323ca5a144360e79834e; USER_FLAG_CHECK=68cf30c1314679791bc6a20432b463cd; abtest=20160909005036905_38; __jda=122270672.1640875838.1473353437272.1473353437272.1473353437272.1; __jdb=122270672.1.1640875838|1.1473353437272; __jdv=122270672|direct|-|none|-; __jdc=122270672; __jdu=1640875838; TrackerID=kQt5mm_szDFmyowGiFDgbK-JmE18IREs_43I8tw7xa77tlHcDQD4UmhDdGhvDBacVBPZWT8WVFbEFfRDO0FRx_4Te_Bicznidv2VNF4Hq5E; pinId=yI9OhuMA-y6BCGhAOQrdPQ; pt_key=AAFX0ZbvADDozUW_Efpt6GNTLiIyRrVIPPZuOuhkHbWQyZERQgpojpmTm_33vYnHBvzzxPyKwVY; pt_pin=18390910719_p; pt_token=hy35alpf; pwdt_id=18390910719_p; whwswswws=e5D3LpJ9C%2FoZAMH0YWaH6QmOqCoCfB53WBTIcW2Rhx6MWRYudj4t6A%3D%3D; returnurl="http://h5.m.jd.com/active/3FEFWVbwgFD97sPwoF6hBnwJyUvr/index.html?coupon=250&win=true&sid=8f1c8d088590323ca5a144360e79834e"; mba_sid=14733534364906122633083450344.3; mba_muid=1473353436489-24e9a0c22668f8912e']
    urls=['http://h5.m.jd.com/h5api.jsp?functionid=babelAwardCollection&body=%7B%22activityId%22%3A%2248ThJmbzxo9EsERuHWfz8QYRPkmY%22%2C%22moduleId%22%3A%22aqdukKyXtgqEQ9wgBsbRR9iCJVt%22%7D&sid=edef42bbd789adbd451f9a80fe67440a&client=wh5&clientVersion=1.0.0&callback=coupon.getState',
          'http://h5.m.jd.com/h5api.jsp?functionid=babelAwardCollection&body=%7B%22activityId%22%3A%2248ThJmbzxo9EsERuHWfz8QYRPkmY%22%2C%22moduleId%22%3A%22aqdukKyXtgqEQ9wgBsbRR9iCJVt%22%7D&sid=8f1c8d088590323ca5a144360e79834e&client=wh5&clientVersion=1.0.0&callback=coupon.getState']
    while True:
        get_page(urls[0],cookies[0])
        get_page(urls[1],cookies[1])