from locust import HttpLocust,Locust,TaskSet,task,between,seq_task
import requests,json,queue,base64,random,os,sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from devops.methodLocust import *

class product(TaskSet):
    '''制品库的用例'''
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
    def task_productCreate(self):
        '''制品库创建'''
        try:
            url = '/paas-web/devopsplatform/productwarehouse/add'
            param = {
                "applicationId":applicationId, #需要动态传参
                "warehouseName":"py-docker-{}".format(self.data["num"]),
                "productType":"".format(str(random.randint(1,4))),   #随机选择制品库类型 1-4个之间随机选择
                "nodeId":"1",
                "delFlag":"0",
                "warehouseId":"0"
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
    def task_productCheck(self):
        '''查询制品库列表'''
        try:
            url = '/paas-web/devopsplatform/productwarehouse/8?applicationId=8&pageNumber=1&pageSize=10&name='
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
    task_set = product       #设置测试类的集合
    wait_time = between(1,5)
    user_data = que()

if __name__ == '__main__':
    os.system('locust -f product.py --host={}'.format(host))