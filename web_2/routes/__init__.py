import os.path
from urllib.parse import quote

from jinja2 import (
    Environment,
    FileSystemLoader,
)

from models.session import Session
from models.user import User
from utils import log


def initialized_environment():
    parent = os.path.dirname(os.path.dirname(__file__))
    path = os.path.join(parent, 'templates')

    loader = FileSystemLoader(path)

    e = Environment(loader=loader)
    return e


class GuaTemplate:
    e = initialized_environment()

    @classmethod
    def render(cls, filename, *args, **kwargs):
        # using get_template load template
        template = cls.e.get_template(filename)

        return template.render(*args, **kwargs)


def current_user(request):
    # username = request.cookies.get('user', User.guest())
    # username = request.cookies.get('user', '【游客】')
    # session_id = request.cookies.get('session_id', '')
    # username = session.get(session_id, User.guest())
    # log('current_user_session_id', session_id)
    # log('current_user_username', username)
    if 'session_id' in request.cookies:
        session_id = request.cookies['session_id']
        log('curr_sess:', session_id)
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


def error(request):
    """
    :return different error request rely on code
    :param request:
    """
    return b'HTTP/1.1 404 NOT FOUND\r\n\r\n<h1>NOT FOUND</h1>'


def formatted_header(headers, code=200):
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


def redirect(url, session_id=None):
    """
    client accept 302, then client check url in location, and request the url
    :param headers:
    :param result:
    :param url:
    :return:
    """
    header = {
        'Location': url,
    }
    if isinstance(session_id, str):
        header.update({
            'Set-Cookie': 'session_id={}; path=/'.format(session_id)
        })

    r = formatted_header(header, 302) + '\r\n'
    return r.encode()


def html_response(filename, **kwargs):
    body = GuaTemplate.render(filename, **kwargs)
    headers = {
        'Content-Type': 'text/html',
    }
    header = formatted_header(headers)
    r = header + '\r\n' + body
    return r.encode()


def login_required(route_function):
    def f(request):
        u = current_user(request)
        if u.is_guest():
            return redirect('/todo/index')
        else:
            return route_function(request)
    return f


def admin_required(route_function):
    def f(request):
        u = current_user(request)
        if u.is_admin():
            return route_function(request)
        else:
            return redirect('/user/login/index')
    return f
