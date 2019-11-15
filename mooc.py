import requests,time
requests.packages.urllib3.disable_warnings()
from io import BytesIO
from PIL import Image,ImageDraw,ImageChops
from lxml import etree
from urllib.parse import urlparse, parse_qs

#大概支持多个课程了吧。。。大概。。。

s = requests.Session()
s.headers.update({'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36'})

def main():
    getuserdata()
    url = 'https://fystat-ans.chaoxing.com/log/setlog?personid='+cpi+'&courseId='+courseId+'&classId='+classId+'&encode=' +encode
    i = 0
    while 1:
        web = s.get(url,verify=False)
        time.sleep(5)
        i+=1
        print(i)
        if(i == 500):
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
            'fid':'1467',    #修改院校，1467:a系统
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
    name = h1.xpath('//h3[@class = "clearfix"]/a/text()')
    print("-----------课程名称-----------")
    print(name)
    print("------------------------------")
    global count
    try:
        count
    except NameError:
        count_exist = False
    else:
        count_exist = True
    if(count_exist):
        pass
    else:
        if(len(name) == 1):
            count = 0
        else:
            count = int(input("请用数字选择要访问的课程(从1开始)："))
            if(count == 1):
                count = 0
            else:
                count = count*2-1
    url = 'https://mooc1-1.chaoxing.com' + geturl[count]
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
    print("登录成功后等待访问数慢慢增加")
    try:
        login()
        main()
    except:
        print("登录信息错误，请重启程序")
