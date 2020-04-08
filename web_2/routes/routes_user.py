from urllib.parse import unquote_plus, quote

from flask import (
    flash,
    request,
    session,
    redirect,
    Blueprint,
    render_template,
)
from werkzeug.datastructures import ImmutableMultiDict

from models.session import Session
from routes import (
    current_user,
    # html_response,
    # redirect
)

from utils import log
from models.user import User


# 不要这么 import
# from xx import a, b, c, d, e, f

bp = Blueprint('user', __name__)

@bp.route('/user/login', methods=['POST'])
def login():
    """
    登录页面的路由函数
    """
    log('login, headers', request.headers)
    log('login, cookies', request.cookies)
    user_current = current_user()
    log('current user', user_current)
    form = request.form
    user, result = User.login(form)
    if user.is_guest():
        return redirect('/user/login/view?result={}'.format(result))
    else:
        # session_id = Session.add(user_id=user.id)
        session['user_id'] = user.id
        flash(result)
        return redirect('/user/login/view')


@bp.route('/user/login/view')
def login_view():
    u = current_user()
    # result = request.query.get('result', '')
    # result = unquote_plus(result)

    return render_template(
        'login.html',
        username=u.username,
        # result=result,
    )


@bp.route('/user/register', methods=['POST'])
def register():
    """
    注册页面的路由函数
    """
    form: ImmutableMultiDict = request.form

    u, result = User.register(form.to_dict())
    log('register post', result)
    flash(result)
    flash([repr(u) for u in User.all()])

    return redirect('/user/register/view')


@bp.route('/user/register/view')
def register_view(request):
    # result = request.query.get('result', '')
    # result = unquote_plus(result)

    return render_template('register.html')


# RESTFul
# GET /login login_get
# POST /login login_post
# UPDATE /user login_update
# DELETE /user login_delete
#
# GET /login
# POST /login/view
# POST /user/update
# GET /user/delete

# user_get()
# user_post()
# def user:
#     if method == 'GET':
#         return user_get()
#     else:
#         return user_post()


def route_dict():
    r = {
        '/user/login': login,
        '/user/login/view': login_view,
        '/user/register': register,
        '/user/register/view': register_view,
    }
    return r
