import socket
import _thread
import time

from flask import Flask

# from request import Request
from utils import log

from models.base_model import SQLModel
from secret import secret_key

# from routes import error

from routes.routes_public import bp as public_bp
from routes.routes_user import bp as user_bp
from routes.routes_weibo import bp as weibo_bp





def error_view(error):
    return 'self_set 404'


def current_time():
    time_format = '%Y%m%d %H:%M:%S'
    localtime = time.localtime(int(time.time()))
    formatted = time.strftime(time_format, localtime)
    return dict(current_time=formatted)


def configured_app():
    app = Flask(__name__)
    # app.register_blueprint(public_bp)
    # app.register_blueprint(user_bp)
    # app.register_blueprint(weibo_bp)
    SQLModel.init_db()

    app.errorhandler(404)(error_view)
    # app.template_filter('formatted_time')(current_time)
    app.context_processor(current_time)

if __name__ == '__main__':
    SQLModel.init_db()
    config = dict(
        debug=True,
        host='localhost',
        port=80,
    )
    app = configured_app()
    log('url_map', app.url_map)
    app.run(**config)

# def response_for_path(request):
#     """
#     根据 path 调用相应的处理函数
#     没有处理的 path 会返回 404
#     """
#     r = {}
#     # 注册外部的路由
#     r.update(todo_routes())
#     r.update(weibo_routes())
#     r.update(user_routes())
#     r.update(public_routes())
#     response = r.get(request.path, error)
#     log('request', request, response)
#     return response(request)


# def request_from_connection(connection):
#     request = b''
#     buffer_size = 1024
#     while True:
#         r = connection.recv(buffer_size)
#         request += r
#         # 取到的数据长度不够 buffer_size 的时候，说明数据已经取完了。
#         if len(r) < buffer_size:
#             request = request.decode()
#             log('request\n {}'.format(request))
#             return request


# def process_request(connection):
#     with connection:
#         r = request_from_connection(connection)
#         log('request log:\n <{}>'.format(r))
#         # 把原始请求数据传给 Request 对象
#         request = Request(r)
#         # 用 response_for_path 函数来得到 path 对应的响应内容
#         response = response_for_path(request)
#         log("response log:\n <{}>".format(response))
#         # 把响应发送给客户端
#         connection.sendall(response)


# def run(host, port):
#     """
#     启动服务器
#     """
#     # 初始化 ORM
#     SQLModel.init_db()
#     # 初始化 socket 套路
#     # 使用 with 可以保证程序中断的时候正确关闭 socket 释放占用的端口
#     log('开始运行于', 'http://{}:{}'.format(host, port))
#     with socket.socket() as s:
#         s.bind((host, port))
#         # 监听 接受 读取请求数据 解码成字符串
#         s.listen()
#         # 无限循环来处理请求
#         while True:
#             connection, address = s.accept()
#             # 第二个参数类型必须是 tuple
#             log('ip {}'.format(address))
#             _thread.start_new_thread(process_request, (connection,))


# if __name__ == '__main__':
#     # 生成配置并且运行程序
#     config = dict(
#         host='127.0.0.1',
#         port=3000,
#     )
#     run(**config)
