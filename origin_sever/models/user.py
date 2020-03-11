from models import Model
from utils import log



class User(Model):
    """
    User 是一个保存用户数据的 model
    现在只有两个属性 username 和 password
    """
    def __init__(self, form):
        super().__init__(form)
        self.username = form.get('username', '')
        self.password = form.get('password', '')

    @staticmethod
    def guest():
        return '【游客】'

    def validate_login(self):
        # u = User.all()
        # log('user_u', u)
        # for i in u:
        #     if self.username == i.username and self.password == i.password :
        #         return True
        # return False
        u = User.find_by(username=self.username, password=self.password)
        return u is not None

    def validate_register(self):
        if len(self.username) > 2 and len(self.password) > 2:
            return False
        else:
            # m = '{},'
            return True