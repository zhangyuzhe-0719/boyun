
from devopsPort.devopsLog.logger import devopsLogger
from selenium import webdriver
from time import sleep
import os,time


class element:

    def __init__(self):
        self.driver = webdriver.Chrome()
        self.driver.get('http://10.10.7.6:7373/#/login')
        self.logger = devopsLogger()

        self.excel = ''     #excel名字
        self.sheet = ''     #sheet页名字
        self.func = ''      #需要执行的方法
        self.remark = ''    #错误信息备注
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
        self.operational = dic['operational']
        self.content = dic['content']
        self.windows = dic['windows']
        self.location = dic['location']
        self.element = dic['element']
        self.dynamic_parameter = dic['dynamic_parameter']
        self.excep = dic['except']
        self.except_element = dic['except_element']
        self.except_method = dic['except_method']
        self.driver.implicitly_wait(10)
        # self.driver.maximize_window()
        self.logger.id = self.id
        self.logger.index = self.index
        self.logger.sheet = self.sheet

    def elementby(self,location,element):
        '''
        判断定位方式,定位到相对应的位置
        :param location: 定位方式
        :param element: 定位元素位置
        :return:
        '''
        if location == 'class':
            self.func = self.driver.find_element_by_class_name(element)
        elif location == 'css':
            self.func = self.driver.find_element_by_css_selector(element)
        elif location == 'id':
            self.func = self.driver.find_element_by_id(element)
        elif location == 'name':
            self.func = self.driver.find_element_by_name(element)
        elif location == 'xpath':
            self.func = self.driver.find_element_by_xpath(element)


    def elementOperational(self,operational):
        '''
        进行动作分析执行动作
        :param operational: 传入的动作,点击,输入,清空
        :return:
        '''
        if operational == 'click':
            self.func.click()
        elif operational == 'input':
            self.func.send_keys(self.content)
        elif operational == 'text':
            sleep(2)
            self.responseText = self.func.text
            print(self.responseText)
        elif operational == 'clear':
            self.func.clear()
        elif operational == 'exist':
            self.elementExist()
        self.func = ''

    def elementExist(self):
        '''查找某个值是否存在'''
        try:
            self.elementby(self.location,self.element)
            self.responseText = True
        except Exception:
            self.responseText = False

    def operationalElement(self,location,element,operational):
        '''
        传入位置参数,调用启动的方法
        :param location: 定位方式
        :param element: 定位的位置信息
        :param operational: 进行的动作
        :return:
        '''
        self.elementby(location,element)
        self.elementOperational(operational)
        self.remark = '测试用例通过'
        # sleep(5)
            # print(e)
            # self.remark = '定位元素未找到'
            # self.logger.status('描述:{} {}'.format(
            #     self.describe,self.remark
            # ))

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
        if self.except_element:         #判断结果位置有值则执行下面方法
            excep = self.caseSplit(self.excep)
            self.excep = excep[0]
            self.location = excep[1]
            self.element = self.except_element
        '''默认取值全部是 loction element excep'''
        if self.excep != 'exist':
            self.operationalElement(self.location,self.element,self.excep)
        else:
            self.elementOperational(self.excep)
        judge = self.judge(str(self.except_method[1]))      #执行判断
        if not judge:
            self.elementScreenshot()

    def dynamicOperational(self,dynamic,element,location='xpath'):
        '''
        动态位置信息改变的方法
        :param dynamic: 传入动态的位置和结果  &=text
        :param element: 位置信息
        :param location: 默认为xpath
        :return: 返回处理后的位置
        '''
        dynamic = self.caseSplit(dynamic)
        num_index = element.index(dynamic[0])
        lst = list(element)
        num = 1                       #需要改变的动态参数的位置
        while dynamic[1] != self.responseText:          #循环找到结果相等的值
            lst[num_index] = str(num)
            element = ''.join(lst)
            self.operationalElement(location, element, operational='text')
            num += 1
        return element

    def judge(self,num):
        '''
        判断数字进行预期结果的比对
        :param num: 传入数字 str类型
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
            if self.except_method[0] == self.responseText:
                ifRemark()
            else:
                ifRemark(0)
        elif num == '2':
            if not self.responseText:
                ifRemark()
            else:
                ifRemark(0)
        elif num == '3':
            if not self.responseText:
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
        if self.dynamic_parameter:
            self.element = self.dynamicOperational(self.dynamic_parameter,self.element,location=self.location)
            self.responseText = ''
        self.operationalElement(self.location,self.element,self.operational)
        if self.excep:
            self.elementExcept()
            self.logger.status(self.remark)
            self.responseText = ''      #清空存放的比对值
        else:
            self.logger.status(self.remark)



if __name__ == '__main__':

    from devopsPort.caseExcel.excelDispose import caseExcel
    case = caseExcel()
    case.status('devopsUI测试用例.xlsx')
    print(case.excelDic)
    ele = element()
    for key in case.excelDic:
        ele.sheet = key
        for cas in case.excelDic[key]:
            ele.start(cas)
            ele.elemendStart()
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

