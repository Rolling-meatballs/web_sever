import os

import urllib.parse

from jinja2 import (
    FileSystemLoader,
    Environment,
)

from utils import log
from models.user import User
from models.message import Message
from models.session import Session

import random
# import json


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


def error(request):
    """
    :return different error request rely on code
    :param request:
    """
    return b'HTTP/1.1 404 NOT FOUND\r\n\r\n<h1>NOT FOUND</h1>'


def current_user(request):
    # username = request.cookies.get('user', User.guest())
    # username = request.cookies.get('user', '【游客】')
    # session_id = request.cookies.get('session_id', '')
    # username = session.get(session_id, User.guest())
    # log('current_user_session_id', session_id)
    # log('current_user_username', username)
    if 'session_id' in request.cookies:
        session_id = request.cookies['session_id']
        s = Session.find_by(session_id=session_id)
        if s is None or s.expired():
            return User.guest()
        else:
            user_id = s.user_id
            username = User.find_by(id=user_id)
            if username is None:
                return User.guest()
            else:
                return username
    else:
        return User.guest()


def response_with_headers(headers, code=200):
    """
    Content-Type: text/html
    Set-Cookie: user=gua
    :param headers:
    :return:
    """
    header = 'HTTP/1.x {} VERY OK\r\n'.format(code)
    header += ''.join([
        '{}: {}\r\n'.format(k, v) for k, v in headers.items()
    ])
    return header


def redirect(url, result=None, headers=None):
    """
    client accept 302, then client check url in location, and request the url
    :param headers:
    :param result:
    :param url:
    :return:
    """
    if result is not None:
        result = urllib.parse.quote_plus(result)
        log('redirect result', result)
        url = '{}?result={}'.format(url, result)

    header = {
        'Location': url,
    }
    if headers is not None:
        header.update(headers)

    r = response_with_headers(header, 302) + '\r\n'
    return r.encode()


def html_response(body):
    headers = {
        'Content-Type': 'text/html',
    }
    header = response_with_headers(headers)
    r = header + '\r\n' + body
    return r.encode()


def configured_environment():
    path = os.path.join(os.path.dirname(__file__), 'templates')
    log('test path', __file__, os.path.dirname(__file__), path)

    loader = FileSystemLoader(path)

    e = Environment(loader=loader)
    return e


class GuaTemplate:
    e = configured_environment()

    @classmethod
    def render(cls, filename, **kwargs):
        template = cls.e.get_template(filename)
        return template.render(**kwargs)


def render_response(filename, **kwargs):
    body = GuaTemplate.render(filename, **kwargs)
    return html_response(body)


def route_index(request):
    """
    computing function of index, return the index respect
    """
    header = 'HTTP/1.1 210 VERY OK\r\nContent-TYpe: text/html\r\n'
    body = template('index.html')
    username = current_user(request)
    body = body.replace('{{username}}', username.username)
    r = header + '\r\n' + body
    return r.encode()


def message_view(request):
    message = Message.all()
    result = request.query.get('result', '')
    log('message_result', result)
    return render_response('messages.html', result=result, messages=message)


def add_message_get(request):
    data = request.query
    if len(data) > 0:
        m = Message.new(data)
        log('post_get', data)

        m.save()
    return redirect('/messages/view')


def add_message_post(request):
    data = request.form()
    if len(data) > 0:
        m = Message.new(data)
        log('post', data)
        m.save()
    return redirect('/messages/view')


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


def route_profile(request):
    username = current_user(request)

    if username == User.guest():
        header = 'HTTP/1.1 302 Internal Redirect\r\nContent-Type: text/html\r\nLocation: http://localhost:3000/login\r\n'
        r = header + '\r\n'
    else:
        header = 'HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n'
        information = User.find_by(username=username.username)
        # information = json.dump(information, indent=2, ensure_ascii=False)
        information = '{}'.format(information)
        log('profile information', information)
        body = template('profile.html')
        body = body.replace('{{information}}', information)
        r = header + '\r\n' + body
    return r.encode()


def route_admin(request):
    # admin page
    users = User.all()
    return render_response('users.html', users=users)


def route_admin_update(request):
    form = request.form()
    user_id = int(form['id'])
    new_password = form['password']
    t = User.find_by(id=user_id)
    t.password = new_password
    t.save()

    return redirect('/admin/user')


def login_required(route_function):
    def f(request):
        u = current_user(request)
        if u.is_guest():
            return redirect('/todo')
        else:
            return route_function(request)
    return f


def admin_required(route_function):
    def f(request):
        u = current_user(request)
        if u.is_admin():
            return route_function(request)
        else:
            return redirect('/login/view')
    return f


def route_dict():
    # log('Hi here is route')
    r = {
        '/': route_index,
        '/static': route_static,
        '/message/view': message_view,
        '/message/get': add_message_get,
        '/message/post': add_message_post,
        '/profile': route_profile,
        '/admin/user': admin_required(route_admin),
        '/admin/user/update': admin_required(route_admin_update),
    }

    return r
