from utils import log
from models.massage import Message
from models.user import User

import random

session = {}


def randon_string():
    """
    生成一个随机的字符串
    :return:
    """
    seed = 'sdfsfasfwebfhtrgfsdfdsa'
    s = ''
    for i in range(16):
        random_index = random.randint(0, len(seed) - 2)
        s += seed[random_index]
    return s


def template(name):
    """
    根据名字取 template 文件夹里的一个文件并返回
    """
    path = 'templates/' + name
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()


def current_user(request):
    # username = request.cookies.get('user', User.guest())
    # username = request.cookies.get('user', '【游客】')
    session_id = request.cookies.get('session_id', '')
    username = session.get(session_id, User.guest())
    return username


def resqonse_with_headers(headers):
    """
    Content-Type: text/html
    Set-Cookie: user=gua
    """
    header = 'HTTP/1.x 210 VERY OK\r\n'
    header += ''.join([
        '{}: {}\r\n'.format(k, v) for k, v in headers.items()
    ])
    return header


def route_index(request):
    """
    主页处理函数， 返回主页的响应
    """
    header = 'HTTP/1.1 210 VERY OK\r\nContent-Type: text/html\r\n'
    body = template('index.html')
    username = current_user(request)
    body =body.replace('{{username}}', username)
    r = header + '\r\n' + body
    return r.encode()


def route_login(request):
    headers = {
        'Content-Type: text/html',
    }
    log('login, headers', request.headers)
    log('login, cookies', request.cookies)
    username = current_user(request)
    if request.method == 'POST':
        form = request.form()
        u = User(form)
        # form['username'] -> u.username
        if u.validate_login():
            # result = '登陆成功'
            username = u.username
            headers['Set-cookie'] = 'user={}'.format(u.username)
            session_id = randon_string()
            session[session_id] = u.username
            headers['Set-cookie'] = 'session_id={}'.format(session_id)
            result = '登陆成功'
        else:
            result = '用户名或者密码错误'
    else:
        result = ''
    body = template('login.html')
    body = body.replace('{{result}}', result)
    body = body.replace('{{username}}', username)
    header = 'HTTP/1.1 210 VERY OK\r\nContent-Type: text/html\r\n'
    r = header + '\r\n' + body
    return r.encode()


def route_register(request):
    if request.method == 'POST':
        form = request.form()
        u = User.new(form)
        if u.validate_register():
            u.save()
            result = '注册成功<br> <pre>{}</pre>'.format(User.all())
        else:
            result = '用户名或密码长度必须大于2'
    else:
        result = ''
    body = template('register.html')
    body = body.replace('{{result}}', result)
    header = 'HTTP/1.1 210 VERY OK\r\nContent-Type: text/html\r\n'
    r = header + '\r\n' + body
    return r.encode()


# message_list = []


def route_messages(request):
    """
    主页处理函数，返回主页的响应
    """

    log('本次请求的 method', request.method)
    if request.method == 'POST':
        data = request.form()
    elif request.method == 'GET':
        data = request.query
    else:
        raise ValueError('unknown method')

    if 'message' in data:
        log('post', data)
        # 应该在这里保存 message_list
        m = Message.new(data)
        m.save()
        # message_list.append(data)

    header = 'HTTP/1.1 210 VERY OK\r\nContent-Type: text/html\r\n'
    body = template('messages.html')
    # ms = '<br>'.join([str(m) for m in message_list])
    ms = '<br>'.join([str(m) for m in Message.all()])
    body = body.replace('{{message}}', ms)
    r = header + '\r\n' + body
    return r.encode()


def route_static(request):
    """
    静态资源的处理函数，读取图片并生成响应返回
    """
    filename = request.query['file']
    log('filename', filename)
    path = 'static/{}'.format(filename)
    with open(path, 'rb') as f:
        header = b'HTTP/1.1 200 OK\r\nContent-Type: image/git\r\ n'
        r = header + b'\r\n' + f.read()
        return r


def error(request):
    """
    根据 code 返回不同的错误响应
    目前只有 404
    """
    r = b'HTTP/1.1 404 NOT FOUND\r\nContent-Type: text/html\r\n\r\n<h1>NOT FOUND</h1>'
    return r


def route_dict():
    """
    路由字典
    key 是路由（路由就是 path）
    value 是路由处理函数（就是响应）
    """
    r = {
        '/': route_index,
        '/static': route_static,
        '/login': route_login,
        '/register': route_register,
        '/messages': route_messages,
    }

    return r
