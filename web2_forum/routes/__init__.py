from flask import session

from models.user import User
from utils import log

def current_user():
    uid = session.get('user_id', -1)
    u = User.one(id=uid)
    return u

