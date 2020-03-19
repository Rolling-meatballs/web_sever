from utils import (
    log,
    random_string,
)

from models.message import Message
from routes import (
    current_user,
    html_response,
    redirect,
    login_required,
    admin_required,
)


def index(request):
    u = current_user(request)
    return html_response('index.html', username=u.username)


def message_index(request):
    message = Message.all()
    log('message_result', result)
    return html_response('messages.html', messages=message)


def message_add_get(request):
    log('the method', request.method)
    data = request.query
    Message.new(data)
    log('get', data)

    return redirect('/messages/index')


def message_add_post(request):
    data = request.form()
    Message.new(data)
    log('post', data)
    return redirect('/messages/index')


def static(request):
    """
    dispose quart data and read picture then give a report
    """
    log('Hi here is a picture')
    filename = request.query.get('file', 'doge.gif')
    path = 'static/{}'.format(filename)
    with open(path, 'rb') as f:
        header = b'HTTP/1.1 200 OK\r\nContent-Type: image/gif\r\n'
        r = header + b'\r\n' + f.read()
        return r


def route_profile(request):
    username = current_user(request)

    if username == User.guest():
        return redirect('/login/view')
    else:
        information = User.find_by(username=username.username)
        # information = json.dump(information, indent=2, ensure_ascii=False)
    return html_response('profile.html', information=information)


def route_admin(request):
    # admin page
    users = User.all()
    return html_response('users.html', users=users)


def route_admin_update(request):
    form = request.form()
    user_id = int(form['id'])
    new_password = form['password']
    t = User.find_by(id=user_id)
    t.password = new_password
    t.save()

    return redirect('/admin/user')


def route_dict():
    # log('Hi here is route')
    r = {
        '/': index,
        '/static': static,
        '/message/view': message_index,
        '/message/get': message_add_get,
        '/message/post': message_add_post,
        '/profile': login_required(route_profile),
        '/admin/user': admin_required(route_admin),
        '/admin/user/update': admin_required(route_admin_update),
    }

    return r
