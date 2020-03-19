from utils import log

from models import Model
from models.user_role import UserRole

import hashlib


class User(Model):
    def __init__(self, form):
        super().__init__(form)
        self.username = form.get('username', '')
        self.password = form.get('password', '')
        self.note = form.get('note', '')
        self.role = form.get('role', UserRole.normal)
        # self.id = form.get('id', None)

    @staticmethod
    def guest():
        form = dict(
            role=UserRole.guest,
            username='[guest]',
            id=-1,
        )
        u = User(form)
        return u

    def is_guest(self):
        return self.role == UserRole.guest

    def is_admin(self):
        return self.role == UserRole.administer

    @staticmethod
    def salted_password(password, salt='%&*&(*$#$(*&JKHIUKJHF'):
        salted = password + salt
        # log('salted', salted)
        hash = hashlib.sha256(salted.encode()).hexdigest()
        return hash

    @classmethod
    def login(cls, form):
        log('login_form', form)
        salted = cls.salted_password(form['password'])

        u = User.find_by(username=form['username'], password=salted)
        if u is not None:
            result = 'login succeed'
            return u, result
        else:
            result = 'username or password is wrong'
            return User.guest(), result

    # def validate_login(self):
        # users = User.all()
        #
        # for user in users:
        #     if self.username == user.username and self.password == user.password:
        #         return True
        # return False

        # u = User.find_by(username=self.username, password=self.password)
        # return u is not None

        # return self.username == 'gua' and self.password == '123'
    @classmethod
    def register(cls, form):
        valid = len(form['username']) > 2 and len(form['password']) > 2
        if valid:
            form['password'] = cls.salted_password(form['password'])
            u = User.new(form)
            u.save()
            result = 'register is succeed<br> <pre>{}</pre>'.format(User.all())
            return u, result
        else:
            result = 'length of username and password need longer than two'
            return User.guest(), result

    @classmethod
    def update(cls, u, new_password):
        u.password = new_password
        u.save()