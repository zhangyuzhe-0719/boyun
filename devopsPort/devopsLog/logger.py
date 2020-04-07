

import logging,os


class devopsLogger:

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
        self.message = ''                   #用户要输入的内容
        self.sheet = ''
        self.id = ''
        self.index = ''


    def info(self):
        self.loger.info(self.message)


    def debug(self):
        self.loger.debug(self.message)

    def status(self,message,bug='info'):
        self.message = 'sheet:{} id:{} index:{}'.format(self.sheet,self.id,self.index) + message
        if bug != 'info':                          #只要bug等级大于info则录入文件中
            self.loger.addHandler(self.fileLog)
        if bug == 'info':
            self.info()
        elif bug == 'debug':
            self.debug()
        else:
            self.message = 'bug级别选定错误,无法记录日志'
            self.debug()


if __name__ == '__main__':
    a = devopsLogger()
    a.status('1',bug='debug')