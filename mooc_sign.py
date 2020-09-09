import requests,time,json,re,base64
from io import BytesIO
requests.packages.urllib3.disable_warnings()
from PIL import Image,ImageDraw,ImageChops
from lxml import etree
from urllib.parse import urlparse, parse_qs

username = ""   #登录账号
password = ""   #登录密码
sckey = ""      #Server酱推送提醒key

s = requests.Session()
s.headers.update({'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.122 Safari/537.36'})
activates = []

def sign(aid, uid):
    global activates
    url = "https://mobilelearn.chaoxing.com/pptSign/stuSignajax?activeId=" + aid + "&uid=" + uid + "&clientip=&latitude=-1&longitude=-1&appType=15&fid=0"
    res = s.get(url,verify=False)
    if (res.text == "success"):
        print(" 签到成功！")
        if sckey != "":
            data = {
                "text" : "签到成功",
                "desp" : "aid" + str(aid)
                }
            sckeyurl = "http://sc.ftqq.com/"+str(sckey)+".send"
            web = s.post(sckeyurl, data=data, verify=False)
        activates.append(aid)
    elif(res.text == "您已签到过了"):
        print(res.text)
        activates.append(aid)
    else:
        if sckey != "":
            data = {
                "text" : "签到失败",
                "desp" : "aid" + str(aid)
                }
            sckeyurl = "http://sc.ftqq.com/"+str(sckey)+".send"
            web = s.post(sckeyurl, data=data, verify=False)
        print("签到失败")

        
    ##########pc版签到############
    '''
    url = f'https://mobilelearn.chaoxing.com/widget/pcpick/stu/index?courseId='+courseId+'&jclassId='+classId
    web = s.get(url,verify=False)
    h1 = etree.HTML(web.text)
    taskdata = h1.xpath('//dd[@class = "green"]/text()')
    while 1:
        if("签到" in taskdata):
            a = h1.xpath('//div[@id = "startList"]//div[@class = "Mct"]/@onclick')[0]
            aid = re.findall(r'[(](.*?)[)]', a)[0].split(',')[0]
            fid = h1.xpath('//input[@id = "fid"]/@value')[0]
            signurl = f'https://mobilelearn.chaoxing.com/widget/sign/pcStuSignController/preSign?activeId='+aid+'&classId='+classId+'&fid='+fid+'&courseId='+courseId
            web = s.get(signurl,verify=False)
            print(web.text)
            break
        else:
            web = s.get(url,verify=False)
            print("签到暂未开通")
            h1 = etree.HTML(web.text)
            taskdata = h1.xpath('//dd[@class = "green"]/text()')
            time.sleep(3)
    '''

def login():
    global uid,username,password
    if(username == "" or password == ""):
        username = input("登录账号：")
        password = input("登录密码：")
    #旧接口，已失效
    #url="http://i.chaoxing.com/vlogin?passWord="+str(password)+"&userName="+str(username)
    url = f'https://passport2-api.chaoxing.com/v11/loginregister?uname='+str(username)+'&code='+str(password)
    res= s.get(url)
    if("验证通过" in str(res.text)):
        print('Login success!')
        for key, value in res.cookies.items():
            if key=="_uid":
                uid=value
        return s
    else:
        print(username,password)
        print('账号密码有误，请重试。')
        username = ""
        password = ""
        login()


'''
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
        for key, value in s.cookies.items():
            if key == "_uid":
                global uid
                uid=value
        return s
    else:
        print('账号密码或验证码有误，请重试。')
        username = ""
        password = ""
        captchalogin(username,password)
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
            count = int(input("请用数字选择要签到的课程(从0开始)："))
    geturl = h1.xpath('//div[@class = "Mcon1img httpsClass"]/a/@href')
    i = 0
    courseurl = []
    for temp in range(0,len(geturl)):
        if("course" in geturl[i]):
            courseurl.append(geturl[i])
        i += 1
    url = 'https://mooc1-1.chaoxing.com' + courseurl[count]
    url_query = urlparse(url).query
    userdata = dict([(k, v[0]) for k, v in parse_qs(url_query).items()])
    global courseId, classId
    courseId = userdata["courseid"]
    classId = userdata["clazzid"]

def main():
    getuserdata()
    while 1:
        url = f'https://mobilelearn.chaoxing.com/ppt/activeAPI/taskactivelist?courseId='+courseId+'&classId='+classId+'&uid='+str(uid)
        web = s.get(url,verify=False)
        activeList = json.loads(web.text)["activeList"]
        for item in activeList:
            if ("nameTwo" not in item):
                continue
            if (item['activeType'] == 2 and item['status'] == 1):
                signurl = item['url']
                var = signurl.split("&")
                for var1 in var:
                    var2 = var1.split("=")
                    if(var2[0] == "activePrimaryId"):
                        aid = var2[1]
                if (aid not in activates):
                    print("查询到签到 名称:%s 活动时间:%s aid:%s" % (
                        item['nameOne'], item['nameFour'], aid))
                    sign(aid, uid)
            else:
                time.sleep(3)
                print("签到暂未开通")    

if __name__ == "__main__":
    print("登录成功后等待签到开始")
    try:
        #captchalogin(username,password)
        login()
        main()
    except Exception as e:
        print('repr(e):', repr(e))
    
