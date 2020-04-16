from sqlalchemy import (
    Column,
    String,
)

from models import Model
from models.base_model import (
    SQLMixin,
    db,
)
from utils import log


class User(SQLMixin, db.Model):
    """
    User is a model storing user data,
    including two properties now
    """
    username = Column(String(50), nullable=False)
    password = Column(String(256), nullable=False)

    @classmethod
    def salted_password(cls, password, salt='kg&^%%57HF'):
        import hashlib
        def sha256(ascii_str):
            return hashlib.sha256(ascii_str.encode('ascii')).hexdigest()
        hash1 = sha256(password)
        hash2 = sha256(hash1 + salt)
        print('sha256', len(hash2))
        return hash2

    def hashed_pawword(self, pwd):
        import hashlib
        # using ascii code switch to bytes object
        p = pwd.encode('ascii')
        s = hashlib.sha256(p)
        # return hex digest str
        return s.hexdigest()

    @classmethod
    def register(cls, form):
        name = form['username']
        password = form['password']
        if len(name) > 2 and User.one(username=name) is None:
            u = User.new(form)
            u.password = u.salted_password(password)
            u.save()
            return u
        else:
            return None

    @classmethod
    def validate_login(cls, form):
        user = User.one(username=form['username'])
        log('validate_login <{}>'.format(form))
        if user is not None and user.password == User.salted_password(form['password']):
            return user
        else:
            return None
