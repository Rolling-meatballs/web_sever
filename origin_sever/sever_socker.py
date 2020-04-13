import importlib
import socket
import _thread
import sys

from request import Request
from utils import log

from models.base_model import SQLModel


def request_from_connection(connection):
    request = b''
    buffer_size = 1024
    while True:
        r = connection.recv(buffer_size)
        request += r
        # 取到的数据长度不够 buffer_size 的时候，说明数据已经取完了。
        if len(r) < buffer_size:
            request = request.decode()
            log('request\n {}'.format(request))
            return request


def process_request(connection, application):
    with connection:
        r = request_from_connection(connection)
        log('request log:\n <{}>'.format(r))
        # 把原始请求数据传给 Request 对象
        request = Request(r)
        # 用 response_for_path 函数来得到 path 对应的响应内容
        response = application(request)
        log("response log:\n <{}>".format(response))
        # 把响应发送给客户端
        connection.sendall(response)


def run(host, port, application):
    """
    启动服务器
    """
    # 初始化 ORM
    SQLModel.init_db()
    # 初始化 socket 套路
    # 使用 with 可以保证程序中断的时候正确关闭 socket 释放占用的端口
    log('开始运行于', 'http://{}:{}'.format(host, port))
    with socket.socket() as s:
        s.bind((host, port))
        # 监听 接受 读取请求数据 解码成字符串
        s.listen()
        # 无限循环来处理请求
        while True:
            connection, address = s.accept()
            # 第二个参数类型必须是 tuple
            log('ip {}'.format(address))
            _thread.start_new_thread(process_request, (connection, application))


if __name__ == '__main__':
    log('wsgi file', sys.argv[1])
    filename = sys.argv[1]
    module = importlib.import_module(filename)
    log('module', module.application)
    # 生成配置并且运行程序
    config = dict(
        host='127.0.0.1',
        port=3000,
        application=module.application
    )
    run(**config)
