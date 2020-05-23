import requests,time,json,re,base64
requests.packages.urllib3.disable_warnings()
from io import BytesIO
from PIL import Image,ImageDraw,ImageChops
from lxml import etree
from urllib.parse import urlparse, parse_qs

username = ""   #登录账号
password = ""   #登录密码

s = requests.Session()
s.headers.update({'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.122 Safari/537.36'})

def captchalogin(username,password):
    if(username == "" or password == ""):
        username = input("登录账号：")
        password = input("登录密码：")
        
    #以下两个用于自动识别验证码，手动输入验证码可无视
    #百度云内的人工智能文字识别orc创建应用获得，不保证识别成功率，可以试试
    APIKey = ""    
    SecretKey = ""
    #免费的每天有api限制
    
    if(APIKey != "" or SecretKey != ""):
        getkeyurl = f'https://aip.baidubce.com/oauth/2.0/token'
        data = {
            "grant_type" : "client_credentials",
            "client_id" : APIKey,
            "client_secret" : SecretKey
            }
        getkey = requests.post(getkeyurl,data).text
        access_token = json.loads(getkey)["access_token"]
        numcode = ""
        while 1:
            t = int(round(time.time()*1000))
            codeurl = f'http://passport2.chaoxing.com/num/code?'+ str(t)
            img_numcode = s.get(codeurl).content
            img = base64.b64encode(img_numcode)
            orcurl = f'https://aip.baidubce.com/rest/2.0/ocr/v1/accurate_basic?access_token='+access_token
            data = {"image":img}
            headers = {'content-type': 'application/x-www-form-urlencoded'}
            captcha = requests.post(orcurl,data=data,headers=headers).text
            numcodelen = json.loads(captcha)["words_result_num"]
            if numcodelen == 0:
                print("验证码识别错误，重新获取验证码识别")
                time.sleep(1)
            else:
                numcode = json.loads(captcha)["words_result"][0]["words"]
                numcode = re.sub("\D","",numcode)
                if len(numcode) < 4:
                    print("验证码识别错误，重新获取验证码识别")
                    time.sleep(1)
                else:
                    print("识别成功")
                    break
    else:
        t = int(round(time.time()*1000))
        url = f'http://passport2.chaoxing.com/num/code?'+ str(t)
        web = s.get(url,verify=False)
        img = Image.open(BytesIO(web.content))
        img.show()
        numcode = input('验证码：')
    url = 'http://passport2.chaoxing.com/login?refer=http://i.mooc.chaoxing.com'
    data = {'refer_0x001': 'http%3A%2F%2Fi.mooc.chaoxing.com',
            'pid':'-1',
            'pidName':'',
            'fid':'1467', #院校id   1467:a系统
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
    time.sleep(2)
    if('账号管理' in str(web.text)):
        print('Login success!')
        return s
    else:
        print('账号密码或验证码有误，请重试。')
        username = ""
        password = ""
        captchalogin(username,password)

'''
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
'''


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
    i=0
    for temp in range(0,len(encodeurl)):
        if("encode" in encodeurl[i]):
            break
        i += 1
    url_query = urlparse(encodeurl[i]).query
    userdata = dict([(k, v[0]) for k, v in parse_qs(url_query).items()])
    encode = userdata["encode"]

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
    

if __name__ == "__main__":
    print("登录成功后等待访问数慢慢增加，显示的数字并不代表访问数，只是用于计数")
    try:
        captchalogin(username,password)
        main()
    except:
        print("登录信息尝试重新登录")
        captchalogin(username,password)
        main()
