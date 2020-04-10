from models.todo_ajax import TodoAjax
from routes import (
    redirect,
    current_user,
    html_response,
    login_required,
    json_response,
)
from utils import log


def index(request):

    u = current_user(request)
    return html_response('todo_ajax_index.html')


def all(request):
    todos = TodoAjax.all()
    todos = [t.__dict__ for t in todos]
    return json_response(todos)


def add(request):
    u = current_user(request)
    form = request.json()
    log('ajax todo add', form, u)
    t = TodoAjax.add(form, u.id)
    message = dict(message='{} added succeed'.format(t.title))
    return json_response(message)

def route_dict():
    d = {
        '/todo/ajax/add': add,
        '/todo/ajax/index': index,
        '/todo/ajax/all': all,
    }
    return d