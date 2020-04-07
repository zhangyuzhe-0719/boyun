from bs4 import BeautifulSoup
import requests

class GetHtml:

    def __init__(self):
        self.url = ''   #对应的url
        self.text = ''


    def start(self,url):
        '''
        启动类方法,传入参数
        :param url:
        :return:
        '''
        self.url = url

    def GetUrl(self):
        '''
        发送请求
        :return: 请求成功赋值text,否则返回None
        '''
        response = requests.get(self.url)
        if response.status_code == 200:
            self.text = response.text
        return None


if __name__ == '__main__':

    a = GetHtml()
    a.start('http://10.10.32.211:9001/')
    a.GetUrl()
    a = BeautifulSoup(a.text,'html.parser')
    a.find_all()
    print(a)
