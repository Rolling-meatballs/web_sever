from urllib.parse import (
    unquote_plus,
    quote,
)

from models.session import Session
from models.sessionSQL import SessionSQL
from models.user import User
from routes import (
    current_user,
    html_response,
    redirect,
    login_required,
    admin_required,
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
    log('test_login')
    form = request.form()
    log('login_routes_form', form)
    user, result = User.login(form)
    if user.is_guest():
        return redirect('/user/login/index?result={}'.format(result))
    else:
        session_id = SessionSQL.save(user.id)
        return redirect('/user/login/index?result={}'.format(result), session_id)


def register_view(request):
    result = request.query.get('result', '')
    result = unquote_plus(result)

    return html_response('register.html', result=result)


def register(request):
    form = request.form()
    u, result = User.register(form)

    return redirect('/user/register/index?result={}'.format(quote(result)))


def edit_password(request):
    user_current = current_user(request)
    u_all = User.all()
    log('user_u_all:', u_all)
    if user_current.is_admin():
        return html_response('admin_password_edit.html', users=u_all)
    else:
        return redirect('/user/login/index')


def update_user_password(request):
    """
    changing user's password
    :param request:
    :return:
    """
    form = request.form()
    log('admin update', form, form['username'], type(form['username']))
    username = form['username']
    new_password = User.salted_password(form['password'])
    log('admin_update_info:', username, new_password)
    u = User.find_by(username=username)
    log('admin_u:', u)
    if u is not None:
        User.update(u, new_password)
    return redirect('/edit_password')


def route_profile(request):
    user = current_user(request)
    information = User.find_by(username=user.username)
    # information = json.dump(information, indent=2, ensure_ascii=False)
    return html_response('profile.html', information=information)


def password_index(request):
    user = current_user(request)
    # user_id = request.query['id']
    # log('password_index', user_id)
    user_id = str(user.id)
    log('password_index', user_id)
    # user = User.find_by(id=user_id)
    # log('password_user', user)
    return html_response('forget_password.html', user_id=user_id)
    # return html_response('forget_password.html', username=user.username)


def password_update(request):
    # user = current_user(request)
    user_id = int(request.query['id'])
    user = User.find_by(id=user_id)
    new_password = form.new_password
    User.update(user, new_password)
    # return redirect('/user/password')
    return redirect('/user/password?id={}'.format(user_id))


def route_dict():
    d = {
        '/user/login/index': login_view,
        '/user/login': login,
        '/user/register/index': register_view,
        '/user/register': register,
        '/edit_password': admin_required(edit_password),
        '/edit_password/update': admin_required(update_user_password),
        '/profile': login_required(route_profile),
        # '/user/password': login_required(password_index),
        '/user/password/index': password_index,
        # '/user/password/reset': login_required(password_update),
        '/user/password/reset': password_update,
    }
    return d
