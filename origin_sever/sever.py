import socket
import urllib.parse

import _thread


from utils import log


def html_content(path):
    with open(path, encoding='utf-8') as f:
        return f.read()


def route_message():
    """
    主页的处理函数， 返回主页的响应
    """
    header = 'HTTP/1.1 233 OK\r\nContent-Type: text/html\r\n'
    body = html_content('html_basic.html')
    r = '{}\r\n{}'.format(header, body)
    return r.encode()


def route_index():
    header = 'Http/1.1 233 very OK\r\nContent-Type: text/html\r\n'
    body = '<h1>Hello world</h1><img src="doge.gif"/>'
    r = '{}\r\n{}'.format(header, body)
    return r.encode()


def route_image():
    """
    图片处理函数， 读取图片并生成响应返回
    """
    with open('doge.gif', 'rb') as f:
        header = b'HTTP/1.1 200 OK\r\nContent-Type: image/gif\r\n\r\n'
        image = header + f.read()
        return image


def error():
    """
    根据 code 返回不同的错误响应
    目前只有 404
    """
    r = b'HTTP/1.1 404 NOT FOUND\r\nContent-Type: text/html\r\n\r\n<h1>NOT FOUND</h1>'
    return r


def response_for_path(path):
    """
    # http://localhost:3000/
    # http://www.baidu.com/
    根据 path 调用响应的处理函数
    没有处理的 path 会返回404
    """
    r = {
        '/': route_index,
        '/message': route_message,
        '/doge.gif': route_image,
    }
    response = r.get(path, error)

    return response()


def run(host, port):
    """
    启动服务器
    """
    with socket.socket() as s:
        # s.bind 用于绑定
        # 注意 bind 函数的参数是一个 tuple
        s.bind((host, port))
        #无限循环处理请求

        # 套路，先要 s.listen 开始监听
        # 3.6 会自动选一个合适的 listen 参数
        # listen 放在 while 外面
        #接收 读取请求数据 解码成字符串
        s.listen()

        # 用一个无限循环来处理请求
        while True:
            # 当有客户端过来连接的时候， s.accept 函数就会返回 2 个值
            # 分别是 连接 和 客户端 ip 地址
            log('before accept')
            connection, address = s.accept()
            with connection:
                log('after accept')
                #这里只读取了 1024 字节的内容， 应该用一个循环全部读取

                # recv 可以接受客户端发送过来的数据
                # 参数是要接收的字节数
                # 返回值是一个 bytes 类型
                request = connection.recv(1024)
                request = request.decode()
                # bytes 类型调用 decode('utf-8') 来转换成一个字符串（str）
                log('ip and request, {}\n{}'.format(address, request))
                # 因为 chrome 会发送空请求导致 split 得到空 list
                # 所以这里判断一下 split 得到的数据长度
                parts = request.split()
                log('parts', parts)

                if len(parts) > 0:
                    path = parts[1]
                    # 用 response_for_path 函数来得到 path 对应的响应内容
                    response = response_for_path(path)
                    # 把响应发送给客户端
                    connection.sendall(response)
                else:
                    #为了解决 chrome 的空包 bug
                    connection.send(b'')
                    log('收到了一个空请求')

            # # b'' 表示这是一个 bytes 对象
            # # 跟之前先写 str 再 encode 是一样的
            # http_response = "HTTP/1.1 233 dasdadjfs\r\n\r\n<h1>Hello world!</h1>"
            # response = http_response.encode()
            #
            # # 用 sendall 发送给客户端
            # connection.sendall(response)
            # # 发送完毕后，关闭本次连接
            # connection.close()

if __name__ == '__main__':
    config = dict(
        port=3000,
        host='0.0.0.0',
    )

    run(**config)