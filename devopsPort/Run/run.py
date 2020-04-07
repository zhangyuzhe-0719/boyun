from devopsPort.requestsSend import devopsRequests
from devopsPort.caseExcel import excelDispose
from devopsPort.devopsLog import logger
import os


class run:

    def __init__(self):
        self.caseExcel = excelDispose.caseExcel()
        self.reportExcel = excelDispose.excelReport()
        self.logger = logger.devopsLogger()
        self.caseDispose = devopsRequests.caseDispose()
        self.devopsRequests = devopsRequests.devopsRequsts()
        self.devopsRequests.loger = self.logger
        self.config = devopsRequests.config()
        self.config.configRead()
        self.caseDispose.domain = self.config.domain    #传入域名地址
        self.case = {}
        self.response = {}
        self.case_all = {}      #所有excel用例汇总
        self.url = ''
        self.parameter = ''
        self.headers = ''
        self.remark = ''
        self.asert = ''
        self.reportResponse = []  #记录测试报告内数据的模式

    def requestsDispose(self):
        '''处理用例的初始化方法'''
        self.caseDispose.logger = self.logger
        self.caseDispose.fullResponse = self.response
        self.caseDispose.start(self.case)

    def logDispose(self):
        '''log初始化启动方法'''
        self.logger.sheet = self.case['sheet']
        self.logger.id = self.case['id']
        self.logger.index = self.case['index']

    def caseExcel_Dispose(self):
        '''读取全部excel用例的方法'''
        # path = os.path.join(os.path.dirname(os.path.dirname(__file__)),"caseExcel")
        # lstFilename = os.listdir(path)
        # for name in lstFilename:
        #     if '.xlsx' in name and "$" not in name:
        #         path = os.path.join(path,name)
        #         self.caseExcel.status(path)
        #         self.case_all[name] = self.caseExcel.excelDic
        self.caseExcel.status(r"D:\boyun\devopsPort\caseExcel\caogao.xlsx")
        self.case_all["name"] = self.caseExcel.excelDic

    def requestSend(self):
        '''发送请求统一调用方法'''
        self.devopsRequests.statusGet(
            code=self.caseDispose.code,
            url=self.caseDispose.url,
            type=self.caseDispose.type,
            parameter=self.caseDispose.finalParameter,
            header=self.caseDispose.header
        )
        self.response[str(int(self.caseDispose.index))] = self.devopsRequests.response #添加返回值,以编号为头{编号:返回值} 存放在列表中


    def responseExcept(self):
        '''返回值统一处理后比对的方法'''
        try:
            if self.caseDispose.filter:
                self.caseDispose.filterResponse(self.devopsRequests.response)
            else:
                self.caseDispose.response = eval(self.caseDispose.response)
                self.caseDispose.exceptResponse = self.devopsRequests.response
            assert self.caseDispose.response == self.caseDispose.exceptResponse
            self.remark = '测试通过'
            self.logger.status(self.remark)  # 记录备注信息
            self.asert = "True"
        except Exception as e:
            if not self.caseDispose.remark:
                self.remark = '实际结果和预期结果不一致'
                self.logger.status(self.remark)  # 记录备注信息
            self.asert = 'False'


    def testReport(self):
        '''生成测试报告的方法'''
        self.reportExcel.excelAppend(self.reportResponse)



    def caseRequests(self):
        '''读取用例操作方法'''

        for excelName in self.case_all:
            self.reportResponse.append([excelName + '执行excel'])
            sheetCase = self.case_all[excelName]
            for sheetName in sheetCase:
                self.logger.sheet = sheetName
                self.reportResponse.append([sheetName + '执行sheet'])
                varID = "1"
                for case in sheetCase[sheetName]:
                    self.case = case
                    self.logger.id = case["id"]
                    self.logger.index = case["index"]
                    self.requestsDispose()
                    self.remark = self.caseDispose.remark
                    if case['id'] != varID:
                        self.response = {}      #如果是第一个用例清理上一次记录的返回值
                        varID = case["id"]
                    if not self.caseDispose.remark:         #处理用例后备注信息为空代表成功可以发送请求
                        self.requestSend()
                        self.remark = self.devopsRequests.remark
                        if not self.remark:
                            self.responseExcept()
                        else:
                            self.logger.status(self.remark,'debug')
                    if not self.asert:
                        self.asert = 'False'
                    self.reportResponse.append([
                        sheetName,
                        self.caseDispose.id,
                        self.caseDispose.index,
                        self.caseDispose.type,
                        self.caseDispose.url,
                        str(self.caseDispose.finalParameter),
                        str(self.caseDispose.header),
                        str(self.devopsRequests.code),
                        str(self.devopsRequests.response),
                        self.asert,
                        self.remark
                    ])  #添加报告列表里的内容
                    self.caseDispose.finalParameter = ''
                    self.caseDispose.exceptResponse = ''
                    self.caseDispose.response = ''
                    self.caseDispose.remark = ''
                    self.devopsRequests.response = ''
                    self.remark = ''
                    self.asert = ''


    def run(self):
        self.caseExcel_Dispose()
        self.caseRequests()
        self.testReport()



if __name__ == "__main__":
    Run = run()
    Run.run()
    # for val in Run.reportResponse:
    #     print(val)