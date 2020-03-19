from urllib.parse import (
    unquote_plus,
    quote,
)

from models.session import Session
from models.user import User
from routes import (
    current_user,
    html_response,
    redirect,
)
from utils import (
    log,
    random_string,
)


def login_view(request):
    user_current = current_user(request)
    result = request.query.get('result', '')
    result = unquote_plus(result)
    return html_response('login.html', result=result, username=user_current.username)


def login(request):
    form = request.form()
    user_current = current_user(request)
    user, result = User.login(form)
    if user.is_guest():
        return redirect('/user/login/view?result={}'.format(result))
    else:
        session_id = Session.add(user_id=user.id)
        return redirect('/user/login/view?result={}'.format(result), session_id)


def register_view(request):
    result = request.query.get('result', '')
    result = unquote_plus(result)

    return html_response('register.html', result=result)


def register(request):
    form = request.form()
    u, result = User.register(form)

    return redirect('/user/register/view?result={}'.format(quote(result)))


def edit_password(request):
    user_current = current_user(request)
    u_all = User.all()
    log('user_u_all:', u_all)
    if user_current.is_admin():
        return html_response('admin_password_edit.html', users=u_all)
    else:
        return redirect('/login/view')


def update_user_password(request):
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
        new_password = User.salted_password(form['password'])
        log('admin_update_info:', username, new_password)
        u = User.find_by(username=username)
        log('admin_u:', u)
        if u is not None:
            User.update(u, new_password)
        else:
            return redirect('/edit_password')
        return redirect('/edit_password')
    else:
        return redirect('/login/view')


def route_dict():
    d = {
        '/user/login/view': login_view,
        '/user/login': login,
        '/user/register/view': register_view,
        '/user/register': register,
        '/edit_password': edit_password,
        '/edit_password/update': update_user_password,
    }
    return d