from flask import (
    request,
    redirect,
    url_for,
    Blueprint,
)

from routes import current_user

from models.reply import Reply
from utils import log

main = Blueprint('reply', __name__)


@main.route('/add', methods=['POST'])
def add():
    form = request.form.to_dict()
    u = current_user()
    # log('DEBUG', form)
    m = Reply.add(form, user_id=u.id)
    return redirect(url_for('topic.detail', id=m.topic_id))