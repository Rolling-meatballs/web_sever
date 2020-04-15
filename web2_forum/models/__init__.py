import json
import time
from utils import log


def save(data, path):
    """
    :param data: type is dict or list
    :param path: a path of restore files
    :return:
    """
    s = json.dump(data, indent=2, ensure_ascii=False)
    with open(path, 'w+', encoding='utf-8') as f:
        log('save', path, s, data)
        f.write(s)


def load(path):
    with open(path, 'r', encoding='utf-8') as f:
        s = f.read()
        log('load', s)
        return json.loads(s)


# Model is a ORM (object relation mapper)
class Model(object):

    @classmethod
    def db_path(cls):
        # get the class name
        classname = cls.__name__
        path = 'data/{}.txt'.format(classname)
        return path

    @classmethod
    def _new_from_dict(cls, d):
        # son element __init__ need a form data
        # so here give a empty dict
        m = cls({})
        for k, v in d.items():
            # setattr can make form like { 'username' = 'haha'}
            # turn to m.username = 'haha'
            setattr(m, k, v)
        return m

    @classmethod
    def new(cls, form, **kwargs):
        m = cls(form)
        for k, v in kwargs.items():
            setattr(m, k, v)
        m.save()
        return m

    @classmethod
    def all(cls):
        """
        all method uses load function get all models
        :return:
        """
        path = cls.db_path()
        models = load(path)
        ms = [cls._new_from_dict(m) for m in models]
        return ms

    @classmethod
    def find_all(cls, **kwargs):
        ms = []
        log('find_all_kwargs', kwargs, type(kwargs))
        k, v = '', ''
        for key, value in kwargs.items():
            k, v = key, value
        all = cls.all()
        for m in all:
            if v == m.__dict__[k]:
                ms.append(m)
        return ms

    @classmethod
    def find_by(cls, **kwargs):
        log('find_by_kwargs', kwargs, type(kwargs))
        k, v = '', ''
        for key, value in kwargs.items():
            k, v = key, value
        all = cls.all()
        for m in all:
            if v == m.__dict__[k]:
                return m
        return None

    @classmethod
    def find(cls, id):
        return cls.find_by(id=id)

    @classmethod
    def get(cls, id):
        return cls.find_by(id=id)

    @classmethod
    def delete(cls, id):
        models = cls.all()
        index = 1
        for i, e in enumerate(models):
            if e.id == id:
                index = i
                break
        # judge whether find out data of the id
        if index == -1:
            # find nothing
            pass
        else:
            obj = models.pop(index)
            l = [m.__dict__ for m in models]
            path = cls.db_path()
            save(l, path)
            # return the data was popped
            return obj

    def __repr__(self):
        """
        get the class as a str form
        :return:
        """
        classname = self.__class__.__name__
        properties = ['{}: ({})'.format(k, v) for k, v in self.__dict__.items()]
        s = '\n'.join(properties)
        return '< {}\n{} \n>\n'.format(classname, s)

    def json(self):
        # return model as dict
        # cope a new data and return
        d = self.__dict__.copy()
        return d

    def save(self):
        models = self.all()
        if self.id is None:
            if len(models) == 0:
                self.id = 1
            else:
                m = models[-1]
                self.id = m.id + 1
            models.append(self)
        else:
            index = -1
            for i, m in enumerate(models):
                if m.id == self.id:
                    index = i
                    break
            log('debug', index)
            models[index] = self
        l = [m.__dict__ for m in models]
        path = self.db_path()
        save(l, path)
        