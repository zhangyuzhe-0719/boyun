from locust import HttpLocust,Locust,TaskSet,task,between,seq_task
import requests,json,queue,base64,random,sys
# sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from devops.methodLocust import *

@task(1)
class logInformation(TaskSet):
    '''日志中心'''
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
    def task_logCheck(self):
        try:
            url = '/paas-web/generalpurposeapi/accesslog/listAccessLog?vagueField=&userId=777&pageNum=1&pageSize=10&isRisk=&startDate=&endDate='
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
    task_set = logInformation       #设置测试类的集合
    wait_time = between(1,5)
    user_data = que()

if __name__ == '__main__':
    import os
    os.system('locust -f logInformation.py --host={}'.format(host))
