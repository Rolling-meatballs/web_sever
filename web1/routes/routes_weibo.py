from flask import (
    request,
    redirect,
    Blueprint,
    render_template,
    url_for,
)

from models.comment import Comment
from models.user import User
from models.weibo import Weibo
from routes import (
    current_user,
    login_required,
)
from utils import log


bp = Blueprint('weibo', __name__)


@bp.route('/weibo/index')
@login_required
def index():
    """
    weibo 首页的路由函数
    """
    # u = current_user()
    # weibos = Weibo.all(user_id=u.id)
    # # 替换模板文件中的标记字符串
    # return html_response('weibo_index.html', weibos=weibos, user=u)
    if 'id' in request.args:
        user_id = int(request.args['id'])
        u = User.one(id=user_id)
    else:
        u = current_user()

    weibos = Weibo.all(user_id=u.id)
    return render_template('weibo_index.html', weibos=weibos, user=u)


@bp.route('/weibo/add', methods=['POST'])
@login_required
def add():
    """
    用于增加新 weibo 的路由函数
    """
    u = current_user()
    form = request.form
    Weibo.add(form, u.id)
    # 浏览器发送数据过来被处理后, 重定向到首页
    # 浏览器在请求新首页的时候, 就能看到新增的数据了
    return redirect('/weibo/index')


@bp.route('/weibo/delete')
def delete():
    weibo_id = int(request.query['id'])
    Weibo.delete(weibo_id)
    # 注意删除所有微博对应评论
    cs = Comment.all(weibo_id=weibo_id)
    for c in cs:
        c.delete()
    return redirect('/weibo/index')


@bp.route('/weibo/edit')
def edit():
    weibo_id = int(request.query['id'])
    w = Weibo.one(id=weibo_id)
    return render_template('weibo_edit.html', weibo=w)


@bp.route('/weibo/update', methods=['POST'])
def update():
    """
    用于增加新 weibo 的路由函数
    """
    form = request.form
    Weibo.update(**form)
    # 浏览器发送数据过来被处理后, 重定向到首页
    # 浏览器在请求新首页的时候, 就能看到新增的数据了
    return redirect('/weibo/index')


@bp.route('/comment/add', methods=['POST'])
@login_required
def comment_add():
    u = current_user()
    form = request.form
    Weibo.comments_add(form, u.id)
    return redirect('/weibo/index')

@bp.route('/comment/delete')
def comment_delete():
    comment_id = int(request.args['id'])
    Comment.delete(comment_id)
    return redirect('/weibo/index')

@bp.route('/comment/edit')
def comment_edit(request):
    comment_id = int(request.query['id'])
    t = Comment.one(id=comment_id)
    return render_template('comment_edit.html', comment=t)

@bp.route('/comment/update', methods=['POST'])
def comment_update():
    """
        用于增加新 weibo 的路由函数
        """
    form = request.form
    Comment.update(**form)
    # 浏览器发送数据过来被处理后, 重定向到首页
    # 浏览器在请求新首页的时候, 就能看到新增的数据了
    return redirect('/weibo/index')

def comment_owner_required(route_function):
    """
    这个函数看起来非常绕，所以你不懂也没关系
    就直接拿来复制粘贴就好了
    """

    def f():
        log('comment_owner_required')
        u = current_user()
        if 'id' in request.args:
            comment_id = request.args['id']
        else:
            comment_id = request.args['id']
        c = Comment.one(id=int(comment_id))

        if c.user_id == u.id:
            return route_function()
        else:
            return redirect(url_for('weibo.index'))

    return f


def weibo_owner_required(route_function):
    """
    这个函数看起来非常绕，所以你不懂也没关系
    就直接拿来复制粘贴就好了
    """

    def f():
        log('weibo_owner_required')
        u = current_user()
        if 'id' in request.args:
            weibo_id = request.args['id']
        else:
            weibo_id = request.args['id']
        w = Weibo.one(id=int(weibo_id))

        if w.user_id == u.id:
            return route_function()
        else:
            return redirect(url_for('weibo.index'))

    return f

def comment_owner_or_weibo_owner_required(route_function):

    def f():
        log('comment_owner_or_weibo_owner_reuired')
        u = current_user()
        if 'id' in request.args:
            comment_id = request.args['id']
        else:
            comment_id = request.args['id']
        c = Comment.one(id=int(comment_id))
        w = Weibo.one(id=c.weibo_id)

        if u.id == c.user_id or u.id == w.user_id:
            return route_function()
        else:
            return redirect(url_for('user.login_view'))

    return f


def route_dict():
    """
    路由字典
    key 是路由(路由就是 path)
    value 是路由处理函数(就是响应)
    """
    d = {
        '/weibo/add': login_required(add),
        '/weibo/delete': login_required(weibo_owner_required(delete)),
        '/weibo/edit': login_required(weibo_owner_required(edit)),
        '/weibo/update': login_required(weibo_owner_required(update)),
        '/weibo/index': login_required(index),
        # 评论功能
        '/comment/add': login_required(comment_add),
        '/comment/delete': login_required(comment_owner_or_weibo_owner_required(comment_delete)),
        '/comment/edit': login_required(comment_owner_required(comment_edit)),
        # '/comment/edit': login_required(comment_edit),
        '/comment/update': login_required(comment_owner_required(comment_update)),
    }
    return d
