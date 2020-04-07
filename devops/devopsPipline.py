
from locust import HttpLocust,Locust,TaskSet,task,between,seq_task
import requests,json,queue,base64,random,os,sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from devops.methodLocust import *

class devopsPipline(TaskSet):
    '''pipline用例'''
    @seq_task(1)
    def task_logging(self):
        '''登录接口'''
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
        except Exception:
            print("请求失败{}".format(res.status_code))

    @seq_task(2)
    def task_createPieline(self):
        '''创建工作流'''
        try:
            url = '/paas-web/pipelineapi/v4/task'
            param = {
                "applicationId":applicationId,
                "taskName":"py-ci{}".format(self.data['num']),
                "serviceId":"1",
                "serviceName":"platform-service",
                "timerV4Vo":{
                    "timerStatus":"1",
                    "timerWeekRate":"",
                    "timerType":"1",
                    "timerTriggerTime":""
                },
                "taskTrigger":"1"
            }
            self.headers = {
                'Content-Type': 'application/json',
                'envId': envid,
                'token':self.token
            }
            res = self.client.post(url,data=json.dumps(param),headers=self.headers)
            response = res.json()
            self.taskId = response["data"]
            print(response)
        except Exception:
            print('请求失败 超时......')



    @seq_task(3)
    def task_pieplineSoud(self):
        '''添加源码管理'''
        try:
            url = '/paas-web/pipelineapi/v4/phase'
            param = {
                "phaseName":"源码管理",
                "taskId":self.taskId
            }
            headers = {
                'Content-Type': 'application/json',
                'token': self.token
            }
            res = self.client.post(url,data=json.dumps(param),headers=headers)
            response = res.json()
            self.phaseId = response['data'] #获取phaseId
            print(response)
        except Exception:
            print('请求失败 超时......')


    @seq_task(4)
    def task_pieplineSoudAdd(self):
        '''源码管理添加'''
        try:
            url = '/paas-web/pipelineapi/v4/stage'
            headers = {
                'Content-Type': 'application/json',
                'token': self.token,
                'envId':envid
            }
            param = {
                'phaseId':self.phaseId,
                'templateId':templateId['拉取代码-通用'],
                'applicationId':applicationId
            }
            res = self.client.post(url,data=json.dumps(param),headers=headers)
            response = res.json()
            print(response)
        except Exception:
            print('请求失败 超时......')


    @seq_task(5)
    def task_pieplineCompile(self):
        '''编译构造'''
        try:
            url = '/paas-web/pipelineapi/v4/phase'
            param = {
                "phaseName":"编译构建",
                "taskId":self.taskId
            }
            headers = {
                'Content-Type': 'application/json',
                'token': self.token
            }
            res = self.client.post(url,data=json.dumps(param),headers=headers)
            response = res.json()
            self.phaseId = response['data'] #获取phaseId
            print(response)
        except Exception:
            print('请求失败 超时......')


    @seq_task(6)
    def task_pieplineCompileAdd(self):
        '''编译构建添加'''
        try:
            url = '/paas-web/pipelineapi/v4/stage'
            headers = {
                'Content-Type': 'application/json',
                'token': self.token,
                'envId':envid
            }
            param = {
                'phaseId':self.phaseId,
                'templateId':templateId['Maven构建-通用'],
                'applicationId':applicationId
            }
            res = self.client.post(url,data=json.dumps(param),headers=headers)
            response = res.json()
            print(response)
        except Exception:
            print('请求失败 超时......')

    @seq_task(7)
    def task_pieplineProduct(self):
        '''制品仓库'''
        try:
            url = '/paas-web/pipelineapi/v4/phase'
            param = {
                "phaseName":"制品仓库",
                "taskId":self.taskId
            }
            headers = {
                'Content-Type': 'application/json',
                'token': self.token
            }
            res = self.client.post(url,data=json.dumps(param),headers=headers)
            response = res.json()
            self.phaseId = response['data'] #获取phaseId
            print(response)
        except Exception:
            print('请求失败 超时......')


    @seq_task(8)
    def task_pieplineProductAdd(self):
        '''制品仓库添加'''
        try:
            url = '/paas-web/pipelineapi/v4/stage'
            headers = {
                'Content-Type': 'application/json',
                'token': self.token,
                'envId':envid
            }
            param = {
                'phaseId':self.phaseId,
                'templateId':templateId['上传制品库-通用'],
                'applicationId':applicationId
            }
            res = self.client.post(url,data=json.dumps(param),headers=headers)
            response = res.json()
            print(response)
        except Exception:
            print('请求失败 超时......')


    @seq_task(9)
    def task_pieplinestart(self):
        '''piepline执行'''
        try:
            url = '/paas-web/pipelineapi/v4/pipeline/build'
            headers = {
                'Content-Type': 'application/json',
                'token': self.token,
                'envId': envid
            }
            param = {"taskId":self.taskId}
            res = self.client.post(url,data=json.dumps(param),headers=headers)
            self.locust.user_data.put_nowait(self.data) #再把参数丢进去
            response = res.json()
            print(response)
        except Exception:
            print('请求失败 超时......')

class situser(HttpLocust):
    '''启动方法'''
    task_set = devopsPipline       #设置测试类的集合
    wait_time = between(1,5)
    user_data = que()

if __name__ == '__main__':
    os.system('locust -f devopsPipline.py --host={}'.format(host))