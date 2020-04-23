import requests,time,re,json
requests.packages.urllib3.disable_warnings()
from lxml import etree
from urllib.parse import urlparse, parse_qs

username = ""   #登录账号
password = ""   #登录密码

s = requests.Session()
s.headers.update({'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.122 Safari/537.36'})
activates = []

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

def sign(aid, uid):
    global activates
    url = "https://mobilelearn.chaoxing.com/pptSign/stuSignajax?activeId=" + aid + "&uid=" + uid + "&clientip=&latitude=-1&longitude=-1&appType=15&fid=0"
    res = s.get(url,verify=False)
    if (res.text == "success"):
        print(" 签到成功！")
        activates.append(aid)
    elif(res.text == "您已签到过了"):
        print(res.text)
        activates.append(aid)
    else:
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
    url="http://i.chaoxing.com/vlogin?passWord="+str(password)+"&userName="+str(username)
    res= s.get(url)
    for key, value in res.cookies.items():
        if key=="_uid":
            uid=value
    web = s.get('http://i.mooc.chaoxing.com/space/index',verify=False)
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
            #count = 1
            count = int(input("请用数字选择要签到的课程(从1开始)："))
            if(count == 1):
                count = 0
            else:
                count = count*2-1
    url = 'https://mooc1-1.chaoxing.com' + geturl[count]
    url_query = urlparse(url).query
    userdata = dict([(k, v[0]) for k, v in parse_qs(url_query).items()])
    global courseId, classId
    courseId = userdata["courseId"]
    classId = userdata["clazzid"]
    

if __name__ == "__main__":
    print("登录成功后等待签到开始")
    try:
        login()
        main()
    except Exception as e:
        print('repr(e):', repr(e))
    
