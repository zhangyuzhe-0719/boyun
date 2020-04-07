import requests,json,logging,os,base64


def bease(data):
    '''
    转换为bs64密文
    :param data:
    :return:
    '''
    bs = base64.b64encode(data.encode("utf-8"))
    passwd = bs.decode("utf-8")
    return passwd

passwd = bease("Zyz0719")       #账号设置的新密码
adminpwd = bease("Bodo123!@#")
usNum = 702     #与实际添加结果  减1

class user:

    def __init__(self,host):
        self.log = log()
        self.host = host
        self.num = ''
        self.email = ""
        self.true = 0
        self.false = 0

    def userLoging(self,user,pwd):
        '''登录'''
        url = self.host + '/paas-web/upmsapi/system/login'
        parme = {'userType': '0',
                 'userName': user,
                 'password': pwd #admin密码:Qm9kbzEyMyFAIw==
                 } #
        res = requests.post(url,data=json.dumps(parme),headers={'Content-Type': 'application/json'})
        response = res.json()
        self.token = response["data"]["userToken"]

    def userCreate(self):
        '''创建用户'''
        url = self.host + "/paas-web/upmsapi/user/create"
        self.userName = 'pycs{}'.format(self.num)
        param = {
            "envId":0,
            "userName":self.userName,
            "userRealName":'zhangyuzhe'.format(self.num),
            "userMail":'ceshi{}@163.com'.format(self.num),
            "userPhone":"1621384{}".format(self.email),
            "userCompany":'',
            "userDept":'',
            "userJobNum":'',
            "orgIds":[]
        }
        self.headers = {
            'Content-Type': 'application/json',
            'token': self.admin_token
        }
        res = requests.post(url,data=json.dumps(param),headers=self.headers)
        if res.status_code == 200:
            self.true += 1
            self.remark = "{} 创建完成状态码:{} 返回值:{}".format(self.num,res.status_code,res.json())
            self.log.status(self.remark)
        else:
            self.false += 1
            self.remark = "{} 创建完成状态码:{} 返回值:{}".format(self.num,res.status_code,res.json())
            self.log.status(self.remark,bug="debug")


    def statusUser(self):
        '''循环创建用户'''
        self.userLoging("admin",adminpwd)
        self.admin_token = self.token
        for i in range(1,usNum):
            '''遍历执行发送请求'''
            self.num = str(i)
            lenNum = len(self.num)
            if lenNum == 1:
                self.email = '00' + self.num
            elif lenNum == 2:
                self.email = '0' + self.num
            else:
                self.email = self.num
            try:
                self.userCreate()
                self.changePasswd(self.userName,passwd)#Wnl6MDcxOQ== 代表新密码Zyz0719
                self.openWrite(self.userName,'Zyz0719')
            except Exception as e:
                self.openWrite(self.userName,'123456')
                self.log.status("{} 未添加成功 报错{}".format(self.num,e),bug="debug")
        print("创建成功用户:{}".format(str(self.true)))
        print("创建失败用户:{}".format(str(self.false)))

    def changePasswd(self,user,newpwd,pwd="MTIzNDU2"):  #密码123456
        '''重置新账号登录密码'''
        self.userLoging(user,pwd)
        self.user_token = self.token
        url = self.host + '/paas-web/upmsapi/user/changePassword'
        param = {
            "password":newpwd,
            "oldPassword":pwd
        }
        headers = {
            'Content-Type': 'application/json',
            'token': self.user_token
        }
        res = requests.post(url,data=json.dumps(param),headers=headers)
        if res.status_code == 200:
            self.remark = "{} {}更改密码成功".format(self.num,user)
            self.log.status(self.remark)
        else:
            self.remark = "{} {}更改密码失败".format(self.num, user)
            self.log.status(self.remark,bug="debug")


    def openWrite(self,num,pwd):
        '''
        写入数据功能
        :param num: 用户名
        :param pwd: 新密码
        :return:
        '''
        with open("logging.txt",mode="a+",encoding="utf-8") as fw:
            fw.write("{},{}\n".format(num,pwd))

    def getUserLSt(self):
        '''获取用户列表'''
        url = self.host + '/paas-web/upmsapi/user/getUsers?userName=&page=1&rows=100'
        headers = {
            'Content-Type': 'application/json',
            'token': self.admin_token
        }
        try:
            res = requests.get(url,headers=headers)
            response = res.json()
            self.MaxUserID = response["data"][0]["userId"]      #拿到最大的userID
            self.log.status("获取用户列表成功,最大userid值:{}".format(self.MaxUserID))
        except Exception as e:
            self.log.status("获取用户失败 报错:{}".format(e))
            exit(0)     #直接退出

    def getProjectLst(self,project):
        '''
        获取租户名称列表
        :param project: 项目名称
        :return:
        '''
        url = self.host + '/paas-web/upmsapi/env/list?envName=&page=1&rows=100'
        headers = {
            'Content-Type': 'application/json',
            'token': self.admin_token
        }
        res = requests.get(url,headers=headers)
        response = res.json()
        try:
            for dic in response["rows"]:
                name = dic["envName"]
                if project == name:
                    self.envId = dic["envId"]
                    self.log.status("租户名称列表获取成功 对应id:{}".format(self.envId))
                    break
        except Exception as e:
            self.log.status("租户获取失败,报错信息:{}".format(e))


    def userAppend(self):
        '''管理员添加'''
        url = self.host + '/paas-web/upmsapi/user/envSpecifyManager'
        lst = []    #存放要添加的数据
        for key in range(self.MaxUserID-usNum-1,self.MaxUserID+1):
            lst.append(key)
        param = {
            'envId': self.envId,
            'userIds': lst
        }
        headers = {
            'Content-Type': 'application/json',
            'token': self.admin_token
        }
        res = requests.post(url,data=json.dumps(param),headers=headers)
        if res.status_code == 200:
            self.log.status("管理员添加数据成功")
        else:
            self.log.status("管理员添加数据失败 {}".format(res.status_code))

    def getApplicationId(self):
        '''获取项目id方法'''
        self.userLoging('pycs2',passwd)
        self.user_token = self.token
        url = self.host + '/paas-web/devopsplatform/application/selectApplication'
        param = {
            "pageVo":{
                "pageNumber":'1',
                "pageSize":'999'
            },
            "envId":[self.envId]
        }
        headers = {
            'Content-Type': 'application/json',
            'token': self.user_token
        }
        res = requests.post(url,data=json.dumps(param),headers=headers)
        response = res.json()
        self.applicationId = response['data']['records'][0]['applicationId']

    def getTemplateId(self):
        '''获取模块名称id 方法 最后返回一个 字典{名称:id}'''
        url = self.host + '/paas-web/pipelineapi/v4/pipelineTaskTemplate?templateType=&templateName=&pageNo=1&pageSize=10'
        headers = {
            'Content-Type': 'application/json',
            'token': self.admin_token
        }
        res = requests.get(url,headers=headers)
        response = res.json()
        lst = response["data"]["rows"]  #获取出模块名称 列表形式
        self.templateIdDic = {}
        for value in lst:
            self.templateIdDic[value["templateName"]] = str(value["templateId"]) #执行按名称存储到数据里

    def userDispose(self,name):
        '''启动方法'''
        self.statusUser() #启动循环
        self.getUserLSt()
        self.getProjectLst(name)
        self.userAppend()
        self.getApplicationId() #获取id
        self.getTemplateId()
        print("evnid :{}".format(self.envId))
        print("applicationId : {}".format(self.applicationId))
        print("timplateName :{}".format(self.templateIdDic))


class log:
    def __init__(self):
        self.path = os.path.join(os.path.dirname(__file__),'Devops.log')
        self.loger = logging.getLogger(self.path)
        self.loger.setLevel(logging.DEBUG)
        self.fileLog = logging.FileHandler(self.path)
        self.fileLog.setLevel(logging.DEBUG)         #定义录入文件 bug级别
        self.cmdLog = logging.StreamHandler()
        self.cmdLog.setLevel(logging.DEBUG)           #定义控制台输入bug 级别
        self.format = logging.Formatter('%(asctime)s %(filename)s %(message)s')
        self.fileLog.setFormatter(self.format)
        self.cmdLog.setFormatter(self.format)           #添加记录日志的前缀
        self.loger.addHandler(self.cmdLog)


    def status(self,message,bug="info"):
        '''记录日志'''
        if bug == "debug":
            self.loger.addHandler(self.fileLog)
            self.loger.debug(message)
        else:
            self.loger.info(message)


if __name__ == "__main__":
    us = user('http://10.10.7.6:8778')
    # us.userDispose("jddy")
    us.userLoging("admin","Qm9kbzEyMyFAIw==")
    us.admin_token = us.token
    us.getUserLSt()
    us.getProjectLst("jddy")
    us.userAppend()
