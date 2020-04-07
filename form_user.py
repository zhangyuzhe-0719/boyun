import random,threading

from_lst = []
from_lst1 = []

num_all = 200000  #代表总共的数据
num_host = 40000   #需要相同的热点数据


def func1():
    '''获取from账号'''
    i = num_all - num_host
    while i > 0:
        from_int = random.randint(1,99999999)
        if from_lst:
            if from_int in from_lst:
                continue  #存在跳过本次循环继续
            else:
                from_lst.append(from_int)
        else:
            from_lst.append(from_int)
        i -= 1      #循环数字-1
        print('添加剩余func1:{}'.format(i))
    for val in range(num_host):
        from_lst.append(2345678)
        print('添加剩余func1:{}'.format(val))

def func2():
    '''获取to账号'''
    i = num_all - num_host
    while i > 0:
        from_int = random.randint(1, 99999999)
        if from_lst1:
            if from_int in from_lst1:
                continue  # 存在跳过本次循环继续
            else:
                from_lst1.append(from_int)
        else:
            from_lst1.append(from_int)
        i -= 1  # 循环数字-1
        print('添加剩余func2:{}'.format(i))
    for val in range(num_host):
        from_lst1.append(2345679)
        print('添加剩余func2:{}'.format(val))

def whiteTxt():
    '''写入文本内容'''
    random.shuffle(from_lst)
    random.shuffle(from_lst1)       #随机排序一次
    txtInt = num_all
    while txtInt > 0:
        fromStr = str(from_lst[txtInt-1])
        toStr = str(from_lst1[txtInt-1])
        if len(fromStr) != 9:
            len_fromStr = 9 - len(fromStr)
            for i in range(len_fromStr):
                fromStr = '0' + fromStr

        if len(toStr) != 9:
            len_toStr = 9 - len(toStr)
            for i in range(len_toStr):
                toStr = '0' + toStr
        #写入文件
        with open('user20.txt',mode='a+',encoding='utf-8') as fw:
            wr = '{},{}\n'.format(fromStr,toStr)
            fw.write(wr)
            print('写入数据:{}'.format(wr))
        txtInt -= 1 #最后结果-1
        print('剩余数量:{}'.format(txtInt))

def run():
    s1 = threading.Thread(target=func1)
    s2 = threading.Thread(target=func2)
    s1.start()
    s2.start()
    s1.join()
    s2.join()
    whiteTxt()


if __name__ == '__main__':
    # run()
    for i in range(10):
        if i ==10:
            def func():
                print(i)


