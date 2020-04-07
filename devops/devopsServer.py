
from locust import HttpLocust,Locust,TaskSet,task,between,seq_task
import requests,json,queue,base64,random,os,sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from devops.methodLocust import *

'''继承TaskSet 统计测试类使用方法'''
class devopServer(TaskSet):
    '''服务管理部分的用例'''

    @seq_task(1)
    def task_logging(self):
        url = '/paas-web/upmsapi/system/login'
        self.data = self.locust.user_data.get_nowait()       #获取先进去的数据
        parme = {'userType': '0',
                 'userName': self.data["name"],
                 'password': bease(self.data["passwd"])
                 }
        res = self.client.post(url,
                                    data=json.dumps(parme),
                                    headers={'Content-Type': 'application/json'})
        response = res.json()
        print(response)
        try:
            assert res.status_code == 200
            self.token = response["data"]["userToken"]
            # res.failure
        except Exception:
            self.token = ''

    @seq_task(2)
    def task_serverCreate(self):
        '''创建一个服务'''
        try:
            url = '/paas-web/devopsplatform/applicationservice/add'
            param = {
                'applicationId':applicationId,        #需要动态处理的
                'serviceName':'py-server{}'.format(self.data['num']),
                'serviceAlias':'pycs{}'.format(self.data['num'])
            }
            headers = {
                'Content-Type': 'application/json',
                'token': self.token
            }
            res = self.client.post(url,data=json.dumps(param),headers=headers)
            response = res.json()
            print(response)
        except Exception:
            print('请求失败 超时......')

    @seq_task(3)
    def task_serverCheck(self):
        '''查询列表'''
        try:
            url = '/paas-web/devopsplatform/applicationservice/8?applicationId=8&pageNumber=1&pageSize=10&name='
            headers = {
                'Content-Type': 'application/json',
                'token': self.token
            }
            res = self.client.get(url,headers=headers)
            self.locust.user_data.put_nowait(self.data) #再把参数丢进去
            response = res.json()
            print(response)
        except Exception:
            print('请求失败 超时......')

class situser(HttpLocust):
    '''启动方法'''
    task_set = devopServer       #设置测试类的集合
    wait_time = between(1,5)
    user_data = que()


if __name__ == '__main__':
    os.system('locust -f {} --host={}'.format(__file__,host))

