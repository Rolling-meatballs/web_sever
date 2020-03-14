from utils import log

from models import Model


class User(Model):
    def __init__(self, form):
        self.username = form.get('username', '')
        self.password = form.get('password', '')
        self.id = form.get('id', None)

    def validate_login(self):
        users = User.all()

        for user in users:
            if self.username == user.username and self.password == user.password:
                return True
        return False

        # return self.username == 'gua' and self.password == '123'

    def validate_register(self):
        return len(self.username) > 2 and len(self.password) > 2