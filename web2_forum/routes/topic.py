from flask import (
    render_template,
    request,
    redirect,
    url_for,
    Blueprint,
)

from routes import current_user

from models.topic import Topic


main = Blueprint('gua_topic', __name__)


@main.route('/')
def index():
    ms = Topic.all()
    return render_template('topic/index.html', ms=ms)


@main.route('/<int:id>')
def detail(id):
    m = Topic.get(id)
    return render_template('topic/detail.html', topic=m)


@main.route('/add', methods=['POST'])
def add():
    form = request.form.to_dict()
    u = current_user()
    m = Topic.add(form, user_id=u.id)
    return redirect(url_for('.detail', id-m.id))


@main.route('/new')
def new():
    return render_template('topic/new.html')