from utils import log
from models.user import User
from models.message import Message

import random

session = {}


def random_string():
    """
    give some strs.
    :return:
    """
    seed = 'lksjdfasnchvieronnmbvmcx'
    s = ''
    for i in range(16):
        random_index = random.randint(0, len(seed) - 2)
        s += seed[random_index]
        return s


def template(name):
    """
    opening a html file named 'name'
    """
    path = 'templates/' + name
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()


def error(request, code=404):
    e = {
        404: b'HTTP/1.1 404 NOT FOUND\r\n\r\n<h1>NOT FOUND</h1>',
    }
    return e.get(code, b'')


def current_user(request):
    username = request.cookies.get('user', User.guest())
    # username = request.cookies.get('user', '【游客】')
    # session_id = request.cookies.get('session_id', '')
    # username = session.get(session_id, User.guest())
    # log('current_user_session_id', session_id)
    log('current_user_cookies', request.cookies)
    log('current_user_username', username)
    # username = session.get(session_id, User.guest())
    return username


def response_with_headers(headers):
    """
    Content-Type: text/html
    Set-Cookie: user=gua
    :param headers:
    :return:
    """
    header = 'HTTP/1.x 210 VERY OK\r\n'
    header += ''.join([
        '{}: {}\r\n'.format(k, v) for k, v in headers.items()
    ])
    return header


def route_index(request):
    """
    computing function of index, return the index respect
    """
    header = 'HTTP/1.1 210 VERY OK\r\nContent-TYpe: text/html\r\n'
    body = template('index.html')
    username = current_user(request)
    body = body.replace('{{username}}', username)
    r = header + '\r\n' + body
    return r.encode()


def route_login(request):
    headers = {
        'Content-Type': 'text/html',
    }
    log('login, headers', request.headers)
    log('login, cookies', request.cookies)
    username = current_user(request)
    if request.method == 'POST':
        form = request.form()
        u = User(form)
        if u.validate_login():
            username = u.username
            headers['Set-Cookie'] = 'user={}'.format(username)
            #session part
            #set a str
            session_id = random_string()
            session[session_id] = username
            headers['Set-Cookie'] = 'session_id={}'.format(session_id)
            result = 'login succeed'
        else:
            result = 'username or password error'
    else:
        result = ''

    body = template('login.html')
    body = body.replace('{{result}}', result)
    body = body.replace('{{username}}', username)
    header = response_with_headers(headers)
    r = '{}\r\n{}'.format(header, body)
    log('login response', r)
    return r.encode()


def route_register(request):
    if request.method == 'POST':
        form = request.form()
        u = User.new(form)
        if u.validate_register():
            u.save()
            result = 'register succeed<br> <pre>{}</pre>'.format(User.all())
        else:
            result = 'length of username and password must bigger than two'
    else:
        result = ''
    body = template('register.html')
    body = body.replace('{{result}}', result)
    header = 'HTTP/1.1 210 VERY OK\r\nContent-Type: text/html\r\n'
    r = header + '\r\n' + body
    return r.encode()


def route_message(request):
    log('session of the times', session)
    username = current_user(request)
    log('Here is user of message', username)
    # if False:
    if username == User.guest():
        return error(request)
    else:
        log('Method of this times', request.method)
        if request.method == 'POST':
            data = request.form()
        elif request.method == 'GET':
            data = request.query
        else:
            raise ValueError('Unknown method')

        if len(data) > 0:
            log('post', data)
            m = Message.new(data)
            m.save()

        header = 'HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n'
        body = template('messages.html')
        ms = '<br>'.join([str(m) for m in Message.all()])
        body = body.replace('{{messages}}', ms)
        r = header + '\r\n' + body
        return r.encode()


def route_static(request):
    """
    dispose quart data and read picture then give a report
    """
    log('Hi here is a picture')
    filename = request.query['file']
    path = 'static/{}'.format(filename)
    with open(path, 'rb') as f:
        header = b'HTTP/1.1 200 OK\r\nContent-Type: image/gif\r\n'
        r = header + b'\r\n' + f.read()
        return r


def route_dict():
    # log('Hi here is route')
    r = {
        '/': route_index,
        '/static': route_static,
        '/login': route_login,
        '/register': route_register,
        '/messages': route_message,
    }

    return r
