
from devopsPort.devopsLog.logger import devopsLogger
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from time import sleep
import os,time


class element:

    def __init__(self):
        self.driver = webdriver.Chrome()
        self.logger = devopsLogger()
        self.mouse = mouse()
        self.mouse.driver = self.driver
        self.driver.maximize_window()
        self.excel = ''     #excel名字
        self.sheet = ''     #sheet页名字
        self.func = ''      #需要执行的方法
        self.remark = ''    #错误信息备注
        self.except_operational = ''    #预期的动作存储
        self.responseText = ''  #查询后返回对比的文本信息

    def start(self,dic):
        '''
        启动方法
        :param dic: 本行用例 字典形式
        :return:
        '''
        self.dic = dic
        self.id = dic['id']
        self.describe = dic['describe']
        self.index = dic['index']
        self.operation_method = dic['operation_method']
        self.operational = dic['operational']
        self.contentOprational(dic)
        self.windows = dic['windows']
        self.method = dic['method']
        self.location = dic['location']
        self.result_operation = dic['result_operation']
        self.element_result = dic['element_result']
        self.element = dic['element']
        self.dynamic_parameter = dic['dynamic_parameter']
        self.except_element = dic['except_element']
        self.except_method = dic['except_method']
        self.driver.implicitly_wait(2)
        # self.driver.maximize_window()
        self.logger.id = self.id
        self.logger.index = self.index
        self.logger.sheet = self.sheet

    def contentOprational(self,dic):
        '''可能存在数字需要转换成字符串'''
        self.content = dic['content']
        if self.content:
            try:
                self.content = int(self.content)
            except Exception:
                pass
            finally:
                self.content = str(self.content)

    def elementby(self,location,element,execute=True,special=''):
        '''
        判断定位方式,定位到相对应的位置
        :param location: 定位方式
        :param element: 定位元素位置
        :param execute: 启动的开关锁,true为启动,false不启动
        :param special: 是否寻找多个位置的方法,默认为空,可以加s
        :return:
        '''
        if location == 'class':
            self.func = "self.driver.find_element{}_by_class_name(element)".format(special)
        elif location == 'css':
            self.func = "self.driver.find_element{}_by_css_selector(element)".format(special)
        elif location == 'id':
            self.func = "self.driver.find_element{}_by_id(element)".format(special)
        elif location == 'name':
            self.func = "self.driver.find_element{}_by_name(element)".format(special)
        elif location == 'xpath':
            self.func = "self.driver.find_element{}_by_xpath(element)".format(special)
        if execute:
            self.func = eval(self.func)

    def elementOperational(self,operational):
        '''
        进行动作分析执行动作
        :param operational: 传入的动作,点击,输入,清空
        :return:
        '''
        if not self.operation_method:
            if operational == 'click':
                self.func.click()
            elif operational == 'input':
                self.func.send_keys(self.content)
            elif operational == 'input_file':
                self.content = os.path.join(os.path.join(os.path.dirname(__file__),'devopsPort'),self.content)
                self.func.send_keys(self.content)
            elif operational == 'text':
                sleep(1)
                self.responseText = self.func.text
                print(self.responseText)
            elif operational == 'clear':
                self.func.clear()
            elif operational == 'get_attribute':
                self.responseText = self.func.get_attribute()
                print(self.responseText)
            elif operational == 'exist':
                self.elementExist()
        elif self.operation_method == 'mouse':
            self.mouse.mouseStart(self.func,operational)
        self.func = ''

    def elementExist(self):
        '''查找某个值是否存在'''
        try:
            self.elementby(self.location,self.element)
            self.responseText = True
        except Exception:
            self.responseText = False

    def loctionElement(self,location,element):
        '''
        用例正常动作处理方法
        :param location: 定位
        :param element: 元素位置
        :return: 最终处理后 都会在self.func生成一个位置
        '''
        if self.dynamic_parameter:
            self.dynamicOperational(self.dynamic_parameter,element,location=location)
            self.responseText = ''
        else:
            self.elementby(location,element)

    def operationalElement(self,location,element,operational):
        '''
        传入位置参数,调用启动的方法
        :param location: 定位方式
        :param element: 定位的位置信息
        :param operational: 进行的动作
        :param method: 默认为true如果需判断改为false
        :return:
        '''
        num = 0
        if self.method:
            lst = self.caseSplit(self.method)
            num = int(lst[1])
        try:
            sleep(num)
            self.loctionElement(location,element)
            self.elementOperational(operational)
            self.remark = '测试用例通过'
        except Exception as e:
            self.remark = '定位有误或动作解析有误,报错:{}'.format(e)
            self.elementScreenshot()

    def elementScreenshot(self):
        '''定位存放文件夹的位置'''
        path = os.path.join(os.path.dirname(os.path.dirname(__file__)),'screenshot')
        mkdir_name = '{}_{}_{}_{}'.format(
            self.excel,self.sheet,self.id,self.index
        )
        screenshot_path = ''
        if os.path.exists(path):
            mkdir_path = os.path.join(path,mkdir_name)
            if not os.path.exists(mkdir_path):
                os.mkdir(mkdir_path)
            screenshot_path = os.path.join(mkdir_path,'截图.png')
        else:
            os.mkdir(path)
            self.elementScreenshot()
        '''截图并保存到对应的位置'''
        self.driver.get_screenshot_as_file(screenshot_path)

    def elementExcept(self):
        '''处理预期结果的方法'''
        self.except_method = self.caseSplit(self.except_method)       #处理成列表形式
        excep = self.except_method.split(";")
        self.excep = excep[1]       #定位动作
        self.location = excep[2]    #定位方式
        self.element = self.except_element
        self.operationalElement(self.location,self.element,self.excep)
        judge = self.judge(str(self.except_method[1]),excep[0])      #执行判断
        if not judge:
            self.elementScreenshot()

    def elementsOperational(self,location,element,operational,element_result):
        '''
        elements  获取到多个元素的时候的处理方法
        :param location: 定位方式
        :param element: 位置
        :param operational 动作
        :param element_result 预期结果
        :return:
        '''
        self.elementby(location, element, execute=True, special='s')
        func = self.func #存储一个临时变量不动
        langFunc = len(self.func)
        for num in range(langFunc):
            self.func = func[num]
            self.elementOperational(operational)
            self.func = func[num]                           #实例两次,上一步动作清空了
            if element_result == self.responseText:
                break

    def dynamicOperational(self,dynamic,element,location='xpath'):
        '''
        动态位置信息改变的方法
        :param dynamic: 传入动态的位置和结果  &=text
        :param element: 位置信息
        :param location: 默认为xpath
        :return: 返回处理后的位置
        '''
        dynamic = self.caseSplit(dynamic)
        operation = dynamic[1].split(";")       #切割 分号 0获取方法 1获取结果
        if dynamic[0]:
            num_index = element.index(dynamic[0])
            lst = list(element)
            num = 1                       #需要改变的动态参数的位置
            while operation[1] != self.responseText:          #循环找到结果相等的值
                lst[num_index] = str(num)
                element = ''.join(lst)
                self.elementsOperational(location,element,operation[0],operation[1])
                num += 1
        else:
            self.elementsOperational(location,element,operation[0],operation[1])

    def judge(self,num,data):
        '''
        判断数字进行预期结果的比对
        :param num: 传入数字 str类型
        :param data: 比对的值
        :return: 返回jug  true或false   代表通过与否
        '''
        jug = ''
        def ifRemark(number=1):
            '''
            判断进行备注信息的填充值
            :param number: 1和0 int形式  默认为1 1是通过 0是不通过
            :return:
            '''
            nonlocal jug
            if number == 1:
                self.remark = '测试通过,比对结果正确'
                jug = True
            else:
                self.remark = '比对结果不正确'
                jug = False
        if num == '1':
            if data == self.responseText:
                ifRemark()
            else:
                ifRemark(0)
        elif num == '2':
            if not self.responseText:
                ifRemark()
            else:
                ifRemark(0)
        elif num == '3':
            if self.except_method[0] in self.responseText:
                ifRemark()
            else:
                ifRemark(0)
        return jug

    def caseSplit(self,data):
        '''
        处理需要分割的字符的方法
        :param data: 需要处理的参数
        :return: 返回处理后的列表
        '''
        def sp(dat,direction='l',obj='=',num=None):
            '''
            分割处理的方法
            :param dat: 需要处理的参数
            :param direction: l代表从左边碰到第一个字符,开始分割  r代表从右边开始 默认为:l
            :param obj: 分割的对象 默认为 =
            :param num: 需要分割的次数,默认为 None
            :return: 返回处理好的列表
            '''
            if 'l' == direction:
                val = dat.split(obj,num)
            else:
                val = dat.rsplit(obj,num)
            return val
        val = sp(data,num=1)
        return val

    def elemendStart(self):
        self.operationalElement(self.location,self.element,self.operational)
        if self.except_element:
            self.elementExcept()
            self.logger.status(self.remark)
            self.responseText = ''      #清空存放的比对值
        else:
            self.logger.status(self.remark)

    def elementGet(self):
        self.driver.get('http://10.10.7.7:7374/#/login')

    def elementClose(self):
        self.driver.close()

class mouse:
    '''鼠标动作常用方法的封装'''
    def __init__(self):
        self.driver = ''
        self.element = ''           #传入定位后的方法
        self.func = ''              #需要最后执行的方法

    def move_to_element(self):
        '''鼠标悬停的方法'''
        self.actionchains.move_to_element(self.element).perform()

    def mouseStart(self,element,operational):
        '''
        鼠标操作方法的启动
        :param element: 定位后的方法
        :param operational: 动作
        :return:
        '''
        self.actionchains = ActionChains(self.driver)       #存入实例
        if operational == 'move_to_element':
            self.element = element
            self.move_to_element()


if __name__ == '__main__':

    from devopsPort.caseExcel.excelDispose import caseExcel
    case = caseExcel()
    case.status('caogao.xlsx')
    print(case.excelDic)
    for key in case.excelDic:
        ele = element()
        ele.sheet = key
        ele.elementGet()
        for cas in case.excelDic[key]:
            ele.start(cas)
            ele.elemendStart()
        ele.elementClose()
    # driver = webdriver.Chrome()
    # driver.get('http://10.10.7.6:7373/#/login')
    # driver.implicitly_wait(5)
    # driver.find_element_by_css_selector('div.el-input.el-input--large.el-input--prefix input.el-input__inner').send_keys('lifubei')
    # sleep(2)
    # driver.find_element_by_css_selector('div.el-input.el-input--large.el-input--prefix input[type=password]').send_keys('Beyondcent@123')
    # sleep(2)
    # driver.find_element_by_css_selector('div.el-form-item__content .dfzq-login,.el-button--primary').click()
    # sleep(2)
    # driver.find_element_by_css_selector('ul.guide li.el-menu-item span.b-Resourcemanagement').click()
    # sleep(2)
    # driver.find_element_by_css_selector('div.devops_header button.el-button,el-button--primary').click()
    # driver.find_element_by_css_selector('div.el-form-item,is-error,is-required div.el-form-item__content div.el-input,el-input--small input.el-input__inner').click()


