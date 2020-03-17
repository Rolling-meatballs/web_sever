import urllib.parse

from models.session import Session
from models.user import User
from routes import (
    response_with_headers,
    template,
    current_user,
    render_response,
    redirect,
)
from utils import (
    log,
    random_string,
)


def login_view(request):
    user_current = current_user(request)
    result = request.query.get('result', '')
    return render_response('login.html', result=result, username=user_current.username)


def login(request):
    form = request.form()
    user_login = User.login_user(form)
    if user_login is not None:
        session_id = Session.add(user_login.id)
        headers = {'Set-Cookie': 'session_id={}'.format(session_id)}
        result = 'login success'
    else:
        result = 'username and password wrong'
        headers = {}

    return redirect('/login/view', result=result, headers=headers)


def register_view(request):
    result = request.query.get('result', '')
    return render_response('register.html', result=result)


def register(request):
    form = request.form()
    u = User.new(form)
    if u.validate_register():
        u.save()
        result = 'register success<br> <pre>{}</pre>'.format(User.all())
    else:
        result = 'length of username and password must longer than two'
    return redirect('/register/view', result=result)


def users(request):
    user_current = current_user(request)
    u_all = User.all()
    log('user_u_all:', u_all)
    if user_current.is_admin():
        return render_response('users.html', users=u_all)
    else:
        return redirect('/login/view')


def update(request):
    """
    changing user's password
    :param request:
    :return:
    """
    user_current = current_user(request)
    if user_current.is_admin():
        form = request.form()
        log('admin update', form, form['username'], type(form['username']))
        username = form['username']
        new_password = form['password']
        log('admin_update_info:', username, new_password)
        u = User.find_by(username=username)
        log('admin_u:', u)
        if u is not None:
            u.password = new_password
            u.save()
        else:
            return redirect('/admin/users')
        return redirect('/admin/users')
    else:
        return redirect('/login/view')


def route_dict():
    d = {
        '/login/view': login_view,
        '/login': login,
        '/register/view': register_view,
        '/register': register,
        '/admin/users': users,
        '/admin/users/update': update,
    }
    return d
