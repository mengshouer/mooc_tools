import requests,time,re,base64,json
from io import BytesIO
from PIL import Image,ImageDraw,ImageChops
from lxml import etree
from urllib.parse import urlparse, parse_qs


username = ""   #登录账号
password = ""   #登录密码

def captchalogin():
    if(username == "" or password == ""):
        username = input("登录账号：")
        password = input("登录密码：")
        
    #以下两个用于自动识别验证码，手动输入验证码可无视
    #百度云内的人工智能文字识别orc创建应用获得
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
    web = s.get('http://i.mooc.chaoxing.com/space/index',verify=False)
    if('账号管理' in str(web.text)):
        print('Login success!')
        return s
    else:
        print('账号密码或验证码有误，请重试。')
        username = ""
        password = ""
        login()
