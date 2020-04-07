
import base64,queue,os
envid = '71'      #租户id
applicationId = '8' #项目id
templateId = {'拉取代码-通用':'72','Sonar提交检查-通用':'73','Maven构建-通用':'75','上传制品库-通用':'76','物理部署-通用':'104','镜像制作-artifactory':'106','容器部署-artifactory':'107'}
host = 'http://10.10.7.6:8778'

def bease(data):
    '''
    转换为bs64密文
    :param data:
    :return:
    '''
    bs = base64.b64encode(data.encode("utf-8"))
    passwd = bs.decode("utf-8")
    return passwd

path = os.path.dirname(__file__)
def que():
    user_data = queue.Queue()
    with open(os.path.join(path,'logging.txt'), mode='r', encoding="utf-8") as fw:
        readData = fw.readlines()  # 读取出来每一行数据,读取全部组装成一个列表
    num = 1
    for value in readData:
        dic = {}
        val = value.strip()
        lst = val.split(',')
        dic["num"] = str(num)
        dic["name"] = lst[0]
        dic["passwd"] = lst[1]
        num += 1
        user_data.put_nowait(dic)  # 直接插入数据
    return user_data
