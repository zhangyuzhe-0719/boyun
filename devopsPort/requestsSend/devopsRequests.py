
import requests,threading,configparser,os,base64,json,copy
from devopsPort.devopsLog.logger import devopsLogger




class devopsRequsts:
    '''发送请求类的封装'''
    def __init__(self):
        self.url = ''           #str
        self.parameter = ''
        self.header = ''
        self.code = ''          #int
        self.type = ''
        self.remark = ''        #备注
        self.loger = ''
        self.response = ''


    def statusGet(self,code,url,type,parameter=None,header=None):
        '''
        启动请求,传入参数
        :param url: 请求的url
        :param parameter:  请求的参数
        :param header: 请求头
        :param code: 状态码
        :return: 无
        '''
        self.url = url
        self.parameter = parameter
        self.header = header
        self.code = code
        self.type = type
        self.response = ''
        self.typeStatus()       #执行调用方法

    def ReqGet(self):
        '''
        普通get请求方式
        :return: 状态和期望相等则返回有值,否则为空
        '''
        val = requests.get(url=self.url, params=self.parameter, headers=self.header)
        self.code = val.status_code
        self.response = val.json()

    def ReqPost(self):
        '''
        普通post请求
        :return: 状态和期望相等则返回有值,否则为空
        '''
        val = requests.post(url=self.url,data=self.parameter,headers=self.header)
        self.code = val.status_code
        self.response = val.json()

    def ReqDelet(self):
        '''
        delete 只需要url
        :return: 状态和期望相等则返回有值,否则为空
        '''
        val = requests.delete(url=self.url,headers=self.header)
        self.code = val.status_code
        self.response = val.json()

    def ReqPut(self):
        '''
        put 请求
        :return: 状态和期望相等则返回有值,否则为空
        '''
        val = requests.put(url=self.url,data=self.parameter,headers=self.header)
        self.code = val.status_code
        self.response = val.json()

    def ReqGetupload(self):
        '''
        上传文件
        :return:
        '''
        pass


    def typeStatus(self):
        try:
            if self.header:
                for key in self.header:
                    if 'json' in self.header[key]:
                        if self.parameter:
                            self.parameter = json.dumps(self.parameter,ensure_ascii=False).encode('utf-8')
            if self.type == 'GET':
                self.ReqGet()
            elif self.type == 'POST':
                self.ReqPost()
            elif self.type == 'DELETE':
                self.ReqDelet()
            elif self.type == 'PUT':
                self.ReqPut()
            else:
                self.remark = '请求类型无法找到'
            if not self.response:
                self.remark = 'code返回错误,无法比对 {}'.format(self.code)
        except Exception as e:
            self.remark = '请求失败,状态码{} {}'.format(self.code,e)


class caseDispose:

    def __init__(self):
        self.caseDic = {}
        self.id = ''
        self.case_scence = ''
        self.cese = ''
        self.index = ''
        self.type = ''
        self.url = ''
        self.parameter = {}
        self.header = ''
        self.body = ''
        self.parameter_dynamic = {}
        self.parameter_value = ''
        self.response= ''
        self.filter = ''
        self.code = ''
        self.finalParameter = ''            #处理后的最终请求值
        self.exceptResponse = ''            #正常返回值 处理后的
        self.domain = ''                    #域名                  需要传
        self.url_data = ''                  #url参数处理
        self.logger = ''        #需要传
        self.remark = ''        #记录备注信息的
        self.fullResponse = {}              #返回值的字典 {'编号':{内容}}     #需要传

    def getDic(self):
        '''
        获取字典每一列的方法,启动
        :return:
        '''
        self.id = int(self.caseDic['id'])
        self.case_scence = self.caseDic['case_scence']
        self.cese = self.caseDic['case']
        self.index = int(self.caseDic['index'])
        self.type = self.caseDic['type']
        self.url = self.caseDic['url']
        self.parameter = self.caseDic['parameter']
        self.header = self.caseDic['header']
        self.body = self.caseDic['body']
        self.parameter_dynamic = self.caseDic['parameter_dynamic']
        self.parameter_value = self.caseDic['parameter_value']
        self.response= self.caseDic['response']
        self.filter = self.caseDic['filter']
        self.code = self.caseDic['code']

    def urlDispose(self):
        '''
        url的处理方法
        :return: 返回到url内添加域名后的地址
        '''
        url_lst = self.url.split(']')
        self.url = self.domain + url_lst[1]         #将域名和url组合
        if '#' in self.url:
            try:
                url = ''
                url_split = url_lst[1].split('/')
                for data in range(len(url_split)):
                    if '#{' in url_split[data]:
                        value = self.stripDispose(url_split[data])
                        url_split[data] = str(self.parameter[value])
                        del self.parameter[value]
                for value in url_split:
                    url = url + value + '/'
                self.url = self.domain + url.rstrip('/')
            except Exception as e:
                self.remark = 'url体内参数未找到对应数据 {}'.format(e)
                self.logger.status('url体内参数未找到对应数据','debug')

    def url_dataDispose(self):
        '''
        url 参数的处理添加  使用type = get,post_body
        :return: 返回到 url_data内url的参数
        '''
        data = ''
        for key in self.parameter:
            data = data + key + '=' + str(self.parameter[key]) + '&'
        self.url = '?' + data.lstrip('&')           #去除末尾的&


    def stripDispose(self,data):
        '''
        不同括号的处理过滤
        :param data: 需要过滤的参数
        :return: 返回处理括号后的
        '''
        value = ''
        if data.startswith('#{'):
            value = data.strip('#{').strip('}')
        elif data.startswith('('):
            value = data.strip('(').strip(')')
        elif data.startswith('['):
            value = data.strip('[').strip(']')
        elif data.startswith('{'):
            value = data.strip('{').strip('}')
        return value

    def parameterDispose(self,data):
        '''
        参数列  body列处理方法
        :param data: 需要处理那一列的数据,传递该位置
        :return: 返回处理后的数据   dic  lstvalue
        '''

        dic = {}
        lstValue = []       #存放数据数据
        def splitDispose(value,type):
            '''
            字典类型处理方法
            :param value: 需要处理的参数
            :param type: 处理类型,dic,lst,str
            :return: 最终返回都是一个列表
            '''
            if type == 'dic':
                st = ','            #需要过滤的标点
            elif type == 'lst':
                st = '&'
            else:
                st = '.'
            lst = []
            if st in value:
                lst =  value.split(st)
            else:
                lst.append(value)
            return lst

        def dynamic(value,key=None,code=True):
            '''
            根据传入参数,处理后获取动态参数里面的值,进行添加
            :param key key值添加字典时对应的key   非必填
            :param value: 需要处理查找啊的动态参数
            :param code: 状态 默认为True 可以改为False  非必填
            :return: code为true进行字典添加,false则返回处理后的value值
            '''
            nonlocal dic
            if '#{' in value:
                value = self.stripDispose(value)
                value = self.parameter_dynamic[value]
            if code:
                dic[key] = value
            else:
                return value

        def lstDispose(value):
            '''
            数组类型数据处理方法,判断动态静态参数
            :param value: 需要进行处理的单个的值
            :return: 最后将数据直接添加到列表中
            '''
            global lstValue
            dicValue = {}
            if value.startswith('{'):
                for val in splitDispose(self.stripDispose(value), 'dic'):
                    key_value = val.split('=', 1)
                    dicValue[key_value[0]] = dynamic(key_value[1], code=False)
                lstValue.append(dicValue)  # 添加到列表中
                dicValue = {}
            elif value.startswith('#{'):
                lstValue.append(dynamic(self.stripDispose(value), code=False))
            else:
                lstValue.append(value)
        '''进行判断处理什么格式的数据'''
        try:
            if not data.startswith('['):
                for value in splitDispose(self.parameter,'dic'):
                    lst = value.split('=', 1)
                    if not lst[1].startswith('[') and not lst[1].startswith('('):
                        dynamic(lst[1],key=lst[0])              #动态参数添加
                    elif lst[1].startswith('('):
                        st = ''
                        for value in splitDispose(self.stripDispose(lst[1]),'str'):
                            st = st + dynamic(value,code=False) + ','
                        dic[lst[1]] = st
                    elif lst[1].startswith('['):
                        array = []      #储存处理后的列表数据
                        for value in splitDispose(self.stripDispose(lst[1]),'lst'):
                            lstDispose(value)       #处理列表单个的值
                        dic[lst[0]] = array         #添加数据到字典中
                return dic
            else:
                for value in splitDispose(self.stripDispose(data),'lst'):
                    lstDispose(value)
                return lstValue
        except Exception as e:
            self.remark = '动态参数格式输入错误或者key值添加未找到'
            self.logger.status('动态参数格式输入错误或者key值添加未找到','debug')

    def paramDynamicDispose(self):
        '''
        处理动态参数办法 调用 paramter_dynamic prameter_value  调用处理成字典
        :return: 将两列的值修改为处理后的字典
        '''
        dic = {}
        #优先判断处理存在 逗号 , 进行分割处理添加\
        lst = []
        def paramSplit(value):
            '''
            判断是否存在逗号,进行分割添加处理
            :param value: 添加要进行判断的参数
            :return: 
            '''
            nonlocal lst
            if ',' in value:
                lst = value.split(',')
            else:
                lst.append(value)

        def paramFor():
            '''
            执行for循环遍历添加数据
            :return: 添加到字典里数据,最后外界调用
            '''
            nonlocal lst,dic
            for data in lst:
                value = data.split('=',1)
                dic[value[0]] = value[1]

        paramSplit(self.parameter_dynamic)      #进行判断
        paramFor()                              #执行数据的循环添加
        self.parameter_dynamic = dic
        lst = []        #清空缓存数据
        dic = {}
        paramSplit(self.parameter_value)
        paramFor()
        self.parameter_value = dic

    def headerDispose(self):
        '''
        请求头的处理方法
        :return: 最终返回到初始化 header里
        '''
        dic = {}
        for value in self.header.split(','):
            lst = value.split('=',1)
            if '#{' in lst[1]:
                dic[lst[0]] = self.parameter_dynamic[self.stripDispose(lst[1])]
            else:
                dic[lst[0]] = lst[1]
        self.header = dic

    def filterDispose(self,data):
        '''
        过滤值和动态参数位置,分割方法,
        :param data: 处理的参数
        :return: 返回处理后的列表,去除特殊符号
        '''
        value = data.split('.')
        value.remove('$')
        return value


    def paramValueDispose(self,key_new,index):
        '''
        动态参数位置进行获取对应需要的参数
        :param index: 对应的id号 int
        :return: 修改对应位置的动态参数
        '''
        index = str(int(index))
        response = self.fullResponse[index]  # 循环最后拿到想要的值
        for key in self.parameter_value:
            try:
                if key == key_new:
                    dynamic = self.parameter_value[key]
                    if '$' in dynamic:
                        for value in self.filterDispose(dynamic):
                            if value:               #必须为有值的状态
                                try:
                                    response = response[value]          #value可能为字符可能为数字
                                except Exception:
                                    value = int(value)
                                    response = response[value]
                        self.parameter_dynamic[key] = response
                        break
            except Exception:
                self.remark = '动态参数位置获取错误,没有找到对应位置参数'
                self.logger.status('动态参数位置获取错误,没有找到对应位置参数','debug')

    def dynamicDispose(self):
        '''
        动态参数统一调用赋值
        :return:
        '''
        self.paramDynamicDispose()
        for key in self.parameter_dynamic:
            ini = int(self.parameter_dynamic[key])
            if ini > 0:
                self.paramValueDispose(key,ini)
            else:
                if ini == -1:
                    bs64 = base64.b64encode(self.parameter_value[key].encode("utf-8"))
                    self.parameter_dynamic[key] = bs64.decode("utf-8")

    def filterResponse(self,response):
        '''
        循环删除返回值里面数据
        :param response: 正常请求后返回的数据
        :return: 删除返回
        '''
        res = copy.deepcopy(response)
        def filSplit(data):
            '''
            判断过滤值是否存在多个值,不管多少哥 最终返回一个列表
            :param data:
            :return:
            '''
            if ',' in data:
                return data.split(',')
            else:
                return [data]
        for value in filSplit(self.filter):
            func = ''
            lst = self.filterDispose(value)
            for key in lst:
                if key:
                    try:
                        key = int(key)
                        func = func + '[' + str(key) + ']'
                    except Exception:
                        func = func + '["' + key + '"]'
            try:
                exec('del res' + func)          #执行添加以后的数据,删除返回值
                try:
                    self.response = eval(self.response)
                except Exception:
                    self.response = json.loads(json.dumps(self.response))
                exec('del self.response' + func)     #删除预期返回值里面数据
            except Exception as e:
                self.remark = '返回值删除过滤值未找到{}'.format(e)
                self.logger.status(self.remark, 'debug')
        self.exceptResponse = res

    def start(self,casedic):
        '''
        类启动处理方法
        :param casedic: 传入用例 字典格式
        :return:
        '''
        self.caseDic = casedic
        self.getDic()                   #启动取餐的方法
        if self.parameter_dynamic:
            self.dynamicDispose()       #调用处理动态参数
        if self.parameter:
            parameter = self.parameterDispose(self.parameter)
            self.parameter = parameter
            self.finalParameter = parameter
        if self.url:
            self.urlDispose()
        if self.body:
            if self.parameter:                  #判断参数列是否还有值,避免url体内参数添加删除后  参数列为空
                self.url_dataDispose()          #将参数添加到url内
            self.finalParameter = self.parameterDispose(self.body)
        if self.header:
            self.headerDispose()




class config:

    def __init__(self):

        self.config = configparser.ConfigParser()
        path = os.path.dirname(os.path.dirname(__file__))
        marge_path = os.path.join(os.path.join(path,'config'),'Config.conf')
        self.config.read(marge_path,encoding='utf-8')
        self.dbDic = {}
        self.domain = ''

    def configRead(self):
        db_items = self.config.items('db')      #读取出关于数据库的配置文件
        for st in db_items:
            self.dbDic[st[0]] = st[1]
        self.domain = self.config.get('by_url','domain')       #获取出域名地址




if __name__ == '__main__':
    c = config()
    c.configRead()
    print(c.domain)
    # c.configRead()
    # caseDispose()
