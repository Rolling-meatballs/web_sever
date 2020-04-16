from flask import (
    request,
    url_for,
    Blueprint,
    render_template,
    redirect,
    session,
    abort,
)

from models.user import User

from routes import current_user

from utils import log


main = Blueprint('index', __name__)


@main.route('/')
def index():
    u = current_user()
    return render_template('index.html', user=u)


@main.route('/register', methods=['POST'])
def register():
    form = request.form
    u = User.register(form)
    return redirect(url_for('.index'))


@main.route('/login', methods=['POST'])
def login():
    log('request', request)
    form = request.form
    log('form', form)
    u = User.validate_login(form)
    log('login user <{}>'.format(u))
    if u is None:
        # turn to topic.index page
        return redirect(url_for('.index'))
    else:
        # writing user_id in session
        session['user_id'] = u.id
        # set cookie permanent for forever
        session.permanent = True
        return redirect(url_for('gua_topic.index'))


@main.route('/profile')
def profile():
    u = current_user()
    if u is None:
        return redirect(url_for('.index'))
    else:
        return render_template('profile.html', user=u)


@main.route('/user/<int:id>')
def user_detail(id):
    u = User.one(id=id)
    if u is None:
        abort(404)
    else:
        return render_template('profile.html', user=u)


def not_found(e):
    return render_template('404.html')