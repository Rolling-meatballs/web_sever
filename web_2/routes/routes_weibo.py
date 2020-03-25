from models.comment import Comment
from models.user import User
from models.weibo import Weibo
from routes import (
    redirect,
    current_user,
    html_response,
    login_required,
)
from utils import log


def index(request):
    s = request.query

    if s == {}:
        u = current_user(request)
        weibos = Weibo.find_all(user_id=u.id)
    else:
        weibos_id = int(request.query['user_id'])
        u = User.find_by(id=weibos_id)
        weibos = Weibo.find_all(user_id=u.id)
    return html_response('weibo_index.html', weibos=weibos, user=u)


def add(request):
    u = current_user(request)
    form = request.form()
    Weibo.add(form, u.id)
    return redirect('/weibo/index')


def delete(request):
    weibo_id = int(request.query['id'])
    Weibo.delete(weibo_id)
    cs = Comment.find_all(weibo_id=weibo_id)

    for c in cs:
        id = int(c.id)
        c.delete(id)
    return redirect('/weibo/index')


def edit(request):
    weibo_id = int(request.query['id|'])
    w = Weibo.find_by(id=weibo_id)
    return html_response('weibo_edit.html', weibo=w)


def update(request):
    form = request.form()
    Weibo.update(form)
    return redirect('/weibo/index')


def comment_add(request):
    u = current_user(request)
    form = request.form()
    weibo_id = int(form['weibo_id'])

    c = Comment(form)
    c.user_id = u.id
    c.weibo_id = weibo_id
    c.save()
    return redirect('/weibo/index')


def comment_delete(request):
    u = current_user(request)
    nuser_id = int(u.id)

    comment_id = int(request.query['id'])
    comments = Comment.find_by(id=comment_id)
    weibo_id = comments.weibo_id
    user_id = comments.user_id

    if nuser_id == user_id or nuser_id == weibo_id:
        Comment.delete(comment_id)
    return redirect('/weibo/index')


def comment_edit(request):
    comment_id = int(request.query['id'])
    t = Comment.find_by(id=comment_id)
    return html_response('comment_edit.html', comment=t)


def comment_update(request):
    form = request.form()
    Comment.update(form)
    return redirect('/weibo/index')


def weibo_owner_required(route_function):

    def f(request):

        u = current_user(request)
        if 'id' in request.query:
            weibo_id = request.query['id']
        else:
            weibo_id = request.form()['id']
        w = Weibo.find_by(id=int(weibo_id))

        if w.user_id == u.id:
            return route_function(request)
        else:
            return redirect('weibo/index')

    return f


def route_dict():

    d = {
        '/weibo/add': login_required(add),
        # '/weibo/delete': delete,
        '/weibo/delete': login_required(weibo_owner_required(delete)),
        '/weibo/edit': login_required(weibo_owner_required(edit)),
        '/weibo/update': login_required(weibo_owner_required(update)),
        '/weibo/index': login_required(index),
        # 评论功能
        '/comment/add': login_required(comment_add),
        '/comment/delete': comment_delete,
        '/comment/edit': comment_edit,
        '/comment/update': comment_update,
    }
    return d