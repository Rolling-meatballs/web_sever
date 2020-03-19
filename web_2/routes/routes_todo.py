from models.todo import Todo

from routes import (
    redirect,
    current_user,
    login_required,
    GuaTemplate,
    html_response,
)

from utils import log
import time


def index(request):
    """
    todo index
    :param request:
    :return:
    """
    u = current_user(request)
    todos = Todo.find_all(user_id=u.id)
    return html_response('todo_index.html', todos=todos)


def add(request):
    """
    add new todo
    :param request:
    :return:
    """
    form = request.form()
    u = current_user(request)

    Todo.add(form, u.id)
    # created_time = Todo.the_time()
    # log('now', created_time)
    # Client retouches the index after update data
    # Client can show new data after give a new request
    return redirect('/todo/index')


def delete(request):
    todo_id = int(request.query['id'])
    Todo.delete(todo_id)
    return redirect('/todo/index')


def edit(request):
    """
    for todo index
    :param request:
    :return:
    """
    # replace tag strings in template files
    todo_id = int(request.query['id'])
    t = Todo.find_by(id=todo_id)
    # body = template('todo_edit.html')
    # body = body.replace('{{todo_id}}', str(todo_id))
    # body = body.replace('{{todo_title}}', str(t.title))

    return html_response('todo_edit.html', todo=t)


def update(request):
    """
    update new todo data
    :param request:
    :return:
    """
    form = request.form()
    log('todo update', form, form['id'], type(form['id']))
    Todo.update(form)

    return redirect('/todo/index')


def same_user_required(route_function):

    def f(request):
        log('same_user_required')
        u = current_user(request)
        if 'id' in request.query:
            todo_id = request.query['id']
        else:
            todo_id = request.form()['id']
        t = Todo.find_by(id=int(todo_id))

        if t.user_id == u.id:
            return route_function(request)
        else:
            return redirect('/todo/index')

    return f


def route_dict():

    d = {
        '/todo/index': index,
        '/todo/add': login_required(add),
        '/todo/delete': login_required(same_user_required(delete)),
        '/todo/edit': login_required(same_user_required(edit)),
        '/todo/update': login_required(same_user_required(update)),
    }
    return d
