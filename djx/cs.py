
import flask,json
from flask import request


class stu:

    def __init__(self):
        self.student = {}
        self.rollback = []      #回退操作
        self.sort_lst = []
        self.return_parm = {"code":200,"data":{}}

    def read(self):
        with open('student.txt', mode='r', encoding='utf-8-sig') as fw:
            lst = fw.readlines()
        for val in lst:
            val_sp = val.split(',')
            name = val_sp[0].encode('utf-8').decode('utf-8-sig')
            self.student[name] = int(val_sp[1].strip())  #添加数据

    #加分 传学生名字
    def mode(self,value):
        for name in value:
            fen = 1
            remark = '加'
            if '+' in name:
                name_lst = name.split('+')
                name = name_lst[0]
                fen = int(name_lst[1])
                self.student[name] = self.student[name] + fen
                remark = '加'
            elif '-' in name:
                name_lst = name.split('-')
                name = name_lst[0]
                fen = int(name_lst[1])
                self.student[name] = self.student[name] - fen
                remark = '扣除'
            self.rollback.append('{},{}'.format(name,str(fen))) #加入回退
            print('{}{}分 {}:{}分'.format(remark,str(fen),name,str(self.student[name])))


    def quit(self):
        with open('../student.txt', mode='w', encoding='UTF8') as fw:
            for name in self.student:
                fw.write(name + ',' + str(self.student[name]) + '\n')

    def roll(self):
        ro_len = len(self.rollback)
        if ro_len != 0:
            ro = self.rollback[ro_len-1].split(',')        #取下标为0 的第一个值
            self.student[ro[0]] = self.student[ro[0]] - int(ro[1])
            del self.rollback[0]
            print('回退成功')
        else:
            print('无法回退,之前没有操作!')


    def sort(self):
        '''排序从高到底'''
        self.sort_lst = []
        for val in self.student:
            self.sort_lst.append('{},{}'.format(val, self.student[val]))
        len_sort = len(self.sort_lst)
        for sort_1 in range(len_sort):
            for sort_2 in range(1,len_sort):
                str2 = self.sort_lst[sort_2]
                sort_str2 = str2.split(',')
                str1 = self.sort_lst[sort_2-1]
                sort_str1 = str1.split(',')
                if int(sort_str2[1]) > int(sort_str1[1]):
                    self.sort_lst[sort_2-1] = str2
                    self.sort_lst[sort_2] = str1




    def run(self,name):
        self.read()
        print(self.student)
        s = 1
            # name = input('增加成绩分的学生名字:')
        if name  == 'q':
            self.quit()
        elif name == 'pr':
            self.sort()
            for value in self.sort_lst:
                print('{}分'.format(value))
            self.sort_lst = []
        elif name == 'roll':
            self.roll()
        else:
            self.mode(name)
        return



app = flask.Flask(__name__,static_url_path='')

s = stu()

@app.route("/",methods=['GET'])
def hi():
    print("返回页面")
    s.read()
    with open("study.html",mode='r',encoding='utf8') as fw:
        rd = fw.read()
        return rd


@app.route('/list',methods=['GET'])
def hello():
    '''
    返回最新的数据
    :return: 返回排序后的数据,从多到少
    '''
    s.sort()
    s.return_parm["data"] = s.sort_lst
    print(s.return_parm)
    return s.return_parm

@app.route('/grade',methods=['POST'])
def grade():
    '''
    分数的修改
    :return:
    '''
    data = json.loads(request.get_data())
    name = data["name"]
    s.mode(name)    #请求然后删除整理数据
    s.return_parm["data"] = "成功"
    return s.return_parm

@app.route('/roll',methods=['GET'])
def roll():
    s.roll()





if __name__ == '__main__':
    app.run(debug=True)
