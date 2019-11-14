import socket
import urllib.parse

import _thread

# from utils import log

s = socket.socket()

# 服务器的 host 为 0.0.0.0, 表示接受任意 ip 地址链接
# port 是端口， 这里设置为2000， 随便选的一个数字

host = '0.0.0.0'
port = 2000

# s.bind 用于绑定
# 注意 bind 函数的参数是一个 tuple
s.bind((host, port))

# 套路，先要 s.listen 开始监听
# 3.6 会自动选一个合适的 listen 参数
# listen 放在 while 外面
s.listen()

# 用一个无限循环来处理请求
while True:

    # 当有客户端过来连接的时候， s.accept 函数就会返回 2 个值
    # 分别是 连接 和 客户端 ip 地址
    print('before accept')
    connection, address = s.accept()
    print('after accept')

    # recv 可以接受客户端发送过来的数据
    # 参数是要接收的字节数
    # 返回值是一个 bytes 类型
    request = connection.recv(1000)

    #bytes 类型调用 decode('utf-8') 来转换成一个字符串（str）
    print('ip and request, {}\n{}'.format(address, request.decode()))

    # b'' 表示这是一个 bytes 对象
    # 跟之前先写 str 再 encode 是一样的
    http_response = "HTTP/1.1 233 dasdadjfs\r\n\r\n<h1>Hello world!</h1>"
    response = http_response.encode()

    # 用 sendall 发送给客户端
    connection.sendall(response)
    # 发送完毕后，关闭本次连接
    connection.close()