import json

from utils import log
from models.user_role import (
    GuaEncoder,
    gua_decode,
)


def save(data, path):
    s = json.dumps(data, indent=2, ensure_ascii=False, cls=GuaEncoder)
    with open(path, 'w+', encoding='utf-8') as f:
        log('save', path, s, data)
        f.write(s)


def load(path):
    with open(path, 'r', encoding='utf-8') as f:
        s = f.read()
        log('load s', type(s), s)
        j = json.loads(s, object_hook=gua_decode)
        log('load j', type(j), j)
        return j


class Model(object):
    def __init__(self, form):
        self.id = form.get('id', None)

    @classmethod
    def db_path(cls):
        classname = cls.__name__
        path = 'db/{}.txt'.format(classname)
        return path

    @classmethod
    def new(cls, form):
        m = cls(form)
        return m

    @classmethod
    def delete(cls, id):
        ms = cls.all()
        for i, m in enumerate(ms):
            if m.id == id:
                del ms[i]
                break

        l = [m.__dict__ for m in ms]
        path = cls.db_path()
        save(l, path)

    @classmethod
    def all(cls):
        path = cls.db_path()
        models = load(path)
        ms = [cls.new(m) for m in models]
        return ms

    @classmethod
    def find_by(cls, **kwargs):
        models = cls.all()
        for model in models:
            exist = True
            for k, v in kwargs.items():
                if not hasattr(model, k) or not getattr(model, k) == v:
                    exist = False
                    break
            if exist:
                return model

    @classmethod
    def find_all(cls, **kwargs):
        models = cls.all()
        result = []
        for model in models:
            exist = True
            for k, v in kwargs.items():
                if not hasattr(model, k) or not getattr(model, k) == v:
                    exist = False
                    break
            if exist:
                result.append(model)

        return result

    def insert(self, models):
        if len(models) > 0:
            self.id = models[-1].id + 1
        else:
            self.id = 0
        models.append(self)

    def update(self, models):
        for i, m in enumerate(models):
            if m.id == self.id:
                models[i] = self
                break

    def save(self):
        models = self.all()
        log('models', models)

        if self.id is None:
            self.insert(models)
        else:
            # self.update(models)
            for i, m in enumerate(models):
                if m.id == self.id:
                    models[i] = self

        data = [m.__dict__ for m in models]
        path = self.db_path()
        save(data, path)

    def __repr__(self):
        classname = self.__class__.__name__
        properties = [
            '{}: ({})'.format(k, v) for k, v in self.__dict__.items()
        ]
        s = '\n'.join(properties)
        return '< {}\n{} >\n'.format(classname, s)
