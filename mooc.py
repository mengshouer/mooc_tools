import requests,time
requests.packages.urllib3.disable_warnings()
from io import BytesIO
from PIL import Image,ImageDraw,ImageChops
from lxml import etree
from urllib.parse import urlparse, parse_qs

#应该只支持同一时间只有一个开放的课程，同时有2个或以上估计得自己填参数

s = requests.Session()
s.headers.update({'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36'})

def main():
    getuserdata()
    url = 'https://fystat-ans.chaoxing.com/log/setlog?personid='+cpi+'&courseId='+courseId+'&classId='+classId+'&encode=' +encode
    url2 = 'https://fystat-ans.chaoxing.com/log/setlog?personid='+cpi+'&courseId='+courseId+'&classId='+classId+'&encode='+encode+'&chapterId=158830768&_=1570014074135'
    i = 0
    while 1:
        web = s.get(url,verify=False)
        time.sleep(5)
        web = s.get(url2,verify=False)
        i+=1
        print(i)
        time.sleep(5)
        if(i == 2000):
            break
    main()


def login():
    username = input("登录账号(请使用手机号登录)：")
    password = input("登录密码：")
    url = "https://passport2.chaoxing.com/num/code"
    web = s.get(url,verify=False)
    img = Image.open(BytesIO(web.content))
    img.show()
    numcode = input('验证码：')
    url = 'http://passport2.chaoxing.com/login?refer=http://i.mooc.chaoxing.com'
    data = {'refer_0x001': 'http%3A%2F%2Fi.mooc.chaoxing.com',
            'pid':'-1',
            'pidName':'',
            'fid':'1467',
            'fidName':'',
            'allowJoin':'0',
            'isCheckNumCode':'1',
            'f':'0',
            'productid':'',
            'uname':username,
            'password':password,
            'numcode':numcode,
            'verCode':''
            }
    web = s.post(url,data=data,verify=False)
    web = s.get('http://i.mooc.chaoxing.com/space/index',verify=False)
    if('账号管理' in str(web.text)):
        print('Login success!')
        return s
    else:
        print('账号密码或验证码有误，请重试。')
        login()


def getuserdata():
    web = s.get('http://mooc1-1.chaoxing.com/visit/courses')
    h1 = etree.HTML(web.text)
    geturl = h1.xpath('//div[@class = "Mcon1img httpsClass"]/a/@href')
    url = 'https://mooc1-1.chaoxing.com' + geturl[0]
    url_query = urlparse(url).query
    userdata = dict([(k, v[0]) for k, v in parse_qs(url_query).items()])
    global cpi, enc, courseId, classId, encode
    cpi = userdata["cpi"]
    enc = userdata["enc"]
    courseId = userdata["courseId"]
    classId = userdata["clazzid"]
    web = s.get(url)
    h2 = etree.HTML(web.text)
    encodeurl = h2.xpath('//script[@type = "text/javascript"]/@src')
    url_query = urlparse(encodeurl[4]).query
    userdata = dict([(k, v[0]) for k, v in parse_qs(url_query).items()])
    encode = userdata["encode"]
    return s

    

if __name__ == "__main__":
    login()
    main()
