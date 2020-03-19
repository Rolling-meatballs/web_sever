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
    s = request.query

