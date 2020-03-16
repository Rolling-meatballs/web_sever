from models.todo import Todo
from models.user import User
from routes import (
    redirect,
    template,
    current_user,
    response_with_headers,
    login_required,
)

from utils import log


def update_request(body):
    headers = {
        'Content-Type': 'text/html',
    }
    header = response_with_headers(headers)
    r = header + '\r\n' + body
    return r.encode()


def index(request):
    """
    todo index
    :param request:
    :return:
    """
    u = current_user(request)
    todos = Todo.find_all(user_id=u.id)

    # give a html
    todo_html = """
        <h3>
            {} : {}
            <a href="/todo/edit?id={}">edit</a>
            <a href="/todo/delete?id={}">delete</a>
        </h3>
    """
    todo_html = ''.join([
        todo_html.format(
            t.id, t.title, t.id, t.id
        ) for t in todos
    ])
    # replace the band staff
    body = template('todo_index.html')
    body = body.replace('{{todos}}', todo_html)

    return update_request(body)


def add(request):
    """
    add new todo
    :param request:
    :return:
    """
    form = request.form()
    u = current_user(request)

    t = Todo.new(form)
    t.user_id = u.id
    t.save()
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
    u = current_user(request)
    if u.is_guest():
        redirect('/todo')
    else:
        # replace tag strings in template files
        todo_id = int(request.query['id'])
        t = Todo.find_by(id=todo_id)
        body = template('todo_edit.html')
        body = body.replace('{{todo_id}}', str(todo_id))
        body = body.replace('{{todo_title}}', str(t.title))

        return update_request(body)


def update(request):
    """
    update new todo data
    :param request:
    :return:
    """
    form = request.form()
    log('todo updata', form, form['id'], type(form['id']))
    todo_id = int(form['id'])
    t = Todo.find_by(id=todo_id)
    t.title = form['title']
    t.save()

    return redirect('/todo')


def route_dict():

    d = {
        '/todo': index,
        '/todo/add': add,
        '/todo/delete': login_required(delete),
        '/todo/edit': login_required(edit),
        '/todo/update': update,
    }
    return d