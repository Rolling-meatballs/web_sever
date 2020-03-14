import json

from utils import log


def save(data, path):
    s = json.dumps(data, indent=2, ensure_ascii=False)
    with open(path, 'w+', encoding='utf-8') as f:
        log('save', path, s, data)
        f.write(s)


def load(path):
    with open(path, 'r', encoding='utf-8') as f:
        s = f.read()
        log('load s', type(s), s)
        j = json.loads(s)
        log('load j', type(j), j)
        return j


class Model(object):
    @classmethod
    def db_path(cls):
        classname = cls.__name__
        path = '{}.txt'.format(classname)
        return path

    @classmethod
    def new(cls, form):
        m = cls(form)
        return m

    @classmethod
    def all(cls):
        path = cls.db_path()
        models = load(path)
        ms = [cls.new(m) for m in models]
        return ms

    def save(self):
        models = self.all()
        log('models', models)
        models.append(self)
        data = [m.__dict__ for m in models]
        path = self.db_path()
        save(data, path)

    @classmethod
    def find_by(cls, **kwargs):
        models = cls.all()
        for model in models:
            if model.username == kwargs:
                return model
        return None

    @classmethod
    def find_all(cls, **kwargs):
        models = cls.all()
        result = []
        for model in models:
            if model.password == kwargs:
                result.append(model)
                continue
        return result

    def __repr__(self):
        classname = self.__class__.__name__
        properties = [
            '{}: ({})'.format(k, v) for k, v in self.__dict__.items()
        ]
        s = '\n'.join(properties)
        return '< {}\n{} >\n'.format(classname, s)


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

class Message(Model):
    def __init__(self, form):
        self.message = form.get('message', '')
        self.author = form.get('author', '')