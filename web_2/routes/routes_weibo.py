from models.comment import Comment
from models.user import User
from model.weibo import Weibo
from routes import (
    redirect,
    current_user,
    html_response,
    login_required,
)
from utils import log


def index(request):
    user = current_user(request)
    user_id = request.quary['user_id']
    weibos = Weibo.find_all(user_id=user_id)
    comments = Comment.find_all()
