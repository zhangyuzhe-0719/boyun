from locust import HttpLocust,Locust,TaskSet,task,between,seq_task
import requests,json,queue,base64,random,os,sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from devops.methodLocust import *

@task(1)
class enviroment(TaskSet):
    '''环境管理用例'''

    @seq_task(1)
    def task_logging(self):
        '''登录'''
        url = '/paas-web/upmsapi/system/login'
        self.data = self.locust.user_data.get_nowait()       #获取先进去的数据
        parme = {'userType': '0',
                 'userName': self.data["name"],
                 'password': bease(self.data["passwd"])
                 }
        res = self.client.post(url,data=json.dumps(parme),headers={'Content-Type': 'application/json'})
        response = res.json()
        print(response)
        try:
            assert res.status_code == 200
            self.token = response["data"]["userToken"]
            # res.failure
        except Exception:
            self.token = ''

    @seq_task(2)
    def task_enviromentCreate(self):
        '''环境创建'''
        try:
            url = '/paas-web/devopsplatform/environment/add'
            num = self.data['num']
            token = self.token
            param = {
                "applicationId":applicationId,        #动态传参的
                "environmentName":'py-env'.format(num),
                "resourceType":'1',
                'containerQuota':{
                    "envType":'1',
                    "cpu":'1',
                    "defaultcpu":'200m',
                    "defaultmem":'256M',
                    "envId":envid,       #动态传参
                    "memory":'1',
                    "pods":'1',
                    "containerId":'',
                    "requeststorage":'1'
                },
                "envType":'1',
                "description":'ceshi'
            }
            headers = {
                'Content-Type': 'application/json',
                'token': token
            }
            res = self.client.post(url,data=json.dumps(param),headers=headers)
            response = res.json()
            print(response)
        except Exception:
            print('请求失败 超时......')

    @seq_task(3)
    def task_enviromentCheck(self):
        '''查询环境列表'''
        try:
            url = '/paas-web/devopsplatform/environment/8?applicationId=8&pageNumber=1&pageSize=10&name='
            headers = {
                'Content-Type': 'application/json',
                'token': self.token
            }
            res = self.client.get(url,headers=headers)
            response = res.json()
            print(response)
            self.locust.user_data.put_nowait(self.data) #再把参数丢进去
        except Exception:
            print('请求失败 超时......')

class situser(HttpLocust):
    '''启动方法'''
    task_set = enviroment       #设置测试类的集合
    wait_time = between(1,5)
    user_data = que()

if __name__ == '__main__':
    os.system('locust -f enviroment.py --host={}'.format(host))