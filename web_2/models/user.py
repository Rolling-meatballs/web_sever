from utils import log

from models import Model
from models.user_role import UserRole


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

    @classmethod
    def login_user(cls, form):

        u = User.find_by(username=form['username'], password=form['password'])
        return u

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

    def validate_register(self):
        return len(self.username) > 2 and len(self.password) > 2
