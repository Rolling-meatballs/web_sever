import functools
import uuid
from functools import wraps

from flask import (
    session,
    request,
    abort,
    redirect,
    url_for,
)

from models.user import User
from routes import current_user
from utils import log


def login_required(route_function):
    @functools.wraps(route_function)
    def f():
        log('login_required')
        u = current_user()
        if u is None:
            log('guest')
            return redirect(url_for('index.index'))
        else:
            log('user', route_function)
            return route_function()

    return f


csrf_tokens = dict()


def csrf_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        token = request.args['token']

        u = current_user()
        if token in csrf_tokens and csrf_tokens[token] == u.id:
            csrf_tokens.pop(token)
            return f(*args, **kwargs)
        else:
            abort(401)

    return wrapper


def new_csrf_token():
    u = current_user()
    token = str(uuid.uuid4())
    csrf_tokens[token] = u.id
    return token