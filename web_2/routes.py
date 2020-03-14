from utils import log
from models import User, Message


def template(name):
    """
    opening a html file named 'name'
    """
    path = 'templates/' + name
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()


def route_index(request):
    """
    computing function of index, return the index respect
    """
    header = 'HTTP/1.1 210 VERY OK\r\nContent-TYpe: text/html\r\n'
    body = template('index.html')
    r = header + '\r\n' + body
    return r.encode()


def route_login(request):
    if request.method == 'POST':
        form = request.form()
        u = User(form)
        if u.validate_login():
            result = 'login succeed'
        else:
            result = 'username or password error'
    else:
        result = ''
    body = template('login.html')
    body = body.replace('{{result}}', result)
    header = 'HTTP/1.1 210 VERY OK\r\nContent-Type: text/html\r\n'
    r = header + '\r\n' + body
    return r.encode()


def route_register(request):
    if request.method == 'POST':
        form = request.form()
        u = User.new(form)
        if u.validate_register():
            if u.id == None:
                u.id = 1
                u.save()
                result = 'register succeed<br> <pre>{}</pre>'.format(User.all())
            else:
                result = 'user exist'
        else:
            result = 'lenght of username and password must bigger than two'
    else:
        result = ''
    body = template('register.html')
    body = body.replace('{{result}}', result)
    header = 'HTTP/1.1 210 VERY OK\r\nContent-Type: text/html\r\n'
    r = header + '\r\n' + body
    return r.encode()


message_list = []


def route_message(request):
    log('method of the times', request.method)
    if request.method == 'POST':
        data = request.form()
    elif request.method == 'GET':
        data = request.query
    else:
        raise ValueError('Unknown method')

    if 'message' in data:
        log('post', data)
        message_list.append(data)

    header = 'HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n'
    body = template('messages.html')
    ms = '<br>'.join([str(m) for m in message_list])
    body = body.replace('{{messages}}', ms)
    r = header + '\r\n' + body
    return r.encode()


def route_static(request):
    """
    dispose quart data and read picture then give a report
    """
    filename = request.query['file']
    path = 'static/{}'.format(filename)
    with open(path, 'rb') as f:
        header = b'HTTP/1.1 200 OK\r\nContent-Type: image/gif\r\n'
        r = header + b'\r\n' + f.read()
        return r


def error(request):
    r = b'HTTP/1.1 404 NOT FOUND\r\nContent-Type: text/html\r\n<h1>NOT FOUND</h1>'
    return r


def route_dict():
    r = {
        '/': route_index,
        '/static': route_static,
        '/login': route_login,
        '/register': route_register,
        '/messages': route_message,
    }

    return r
