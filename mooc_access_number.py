import requests,time
requests.packages.urllib3.disable_warnings()
from io import BytesIO
from PIL import Image,ImageDraw,ImageChops
from lxml import etree
from urllib.parse import urlparse, parse_qs

username = ""   #登录账号
password = ""   #登录密码

s = requests.Session()
s.headers.update({'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.122 Safari/537.36'})

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
    global uid,username,password
    if(username == "" or password == ""):
        username = input("登录账号：")
        password = input("登录密码：")
    url="http://i.chaoxing.com/vlogin?passWord="+str(password)+"&userName="+str(username)
    res= s.get(url)
    for key, value in res.cookies.items():
        if key=="_uid":
            uid=value
    web = s.get('http://i.mooc.chaoxing.com/space/index',verify=False)
    time.sleep(2)
    if('账号管理' in str(web.text)):
        print('Login success!')
        return s
    else:
        print(username,password)
        print('账号密码有误，请重试。')
        username = ""
        password = ""
        login()


def getuserdata():
    web = s.get('http://mooc1-1.chaoxing.com/visit/courses')
    h1 = etree.HTML(web.text)
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
            #count = 0
            count = int(input("请用数字选择要访问的课程(从0开始)："))
    geturl = h1.xpath('//div[@class = "Mcon1img httpsClass"]/a/@href')
    i = 0
    courseurl = []
    for temp in range(0,len(geturl)):
        if("/mycourse/studentcourse" in geturl[i]):
            courseurl.append(geturl[i])
        i += 1
    url = 'https://mooc1-1.chaoxing.com' + courseurl[count]
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
    url_query = urlparse(encodeurl[6]).query
    userdata = dict([(k, v[0]) for k, v in parse_qs(url_query).items()])
    encode = userdata["encode"]

    

if __name__ == "__main__":
    print("登录成功后等待访问数慢慢增加")
    try:
        login()
        main()
    except:
        print("登录信息尝试重新登录")
        login()
        main()
