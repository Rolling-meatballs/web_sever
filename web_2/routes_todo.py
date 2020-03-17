from models.todo import Todo
from models.user import User
from routes import (
    redirect,
    template,
    current_user,
    response_with_headers,
    login_required,
    GuaTemplate,
    html_response,
    render_response,
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
    return render_response('todo_index.html', todos=todos)


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
    return redirect('/todo')


def delete(request):
    todo_id = int(request.query['id'])
    Todo.delete(todo_id)
    return redirect('/todo')


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

    return render_response('todo_edit.html', todo=t)


def update(request):
    """
    update new todo data
    :param request:
    :return:
    """
    form = request.form()
    log('todo updata', form, form['id'], type(form['id']))
    Todo.update(form)

    return redirect('/todo')


def route_dict():

    d = {
        '/todo': index,
        '/todo/add': add,
        '/todo/delete': login_required(delete),
        '/todo/edit': login_required(edit),
        '/todo/update': login_required(update),
    }
    return d