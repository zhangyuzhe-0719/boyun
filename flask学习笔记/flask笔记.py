import self as self
from flask import Flask,abort,make_response,Response

#简单的小程序
'''
flas = Flask(__name__)      #初始化

@flas.route('/hello/<name>')            #route传递url执行方法

#中可以使用的方法
@flas.route(/hello/<string:name>)           传入字符串不包含斜线的字符串
<int:name>  整形数字
<any(red,color,orange):name>     只能掺入name中的参数       

def hello_name(name):
    return '{} hello'.format(name)
    

#请求钩子

before_first_request    注册一个函数,在处理第一个请求前执行  
进行一些初始化的操作

before_request          注册一个函数,在处理每个请求前运行

after_request           注册一个函数,在没有未处理的报错情况下,每个请求后执行

teardown_request        注册一个函数,在有报错未处理的情况下,每个请求结束后执行,发生异常会传入异常对象作为参数

after_this_request      在视图函数内注册一个函数,会在这个请求结束后运行

url_for('hello')            返回 /hello  完整的url

redirect('url')              输入完整的url跳转到对应的url中

from flask import abort   
abort(404)              自定义返回得状态码


from flask import make_response

response = make_reponse('')         #设置要返回的值
response.mimetype = 'application/json'      设置ContentType 的属性
response.set_cookie()               设置要传入的cookie
key,            键值
value="",       值
max_age=None,   保存时间单位为 秒
expires=None,   过期时间,datatime对象
path="/",
domain=None,
secure=None,
httponly=False,
charset="utf-8",


from flask import g

g变量 存放当前请求可用的,每次请求后都会重设
    
'''
app = Flask(__name__)
class devOps:

    def __init__(self):
        pass

    @app.route('/hello')
    def hello(self):
        return '开始'
