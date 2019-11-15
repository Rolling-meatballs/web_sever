import json

from utils import log


def save(data, path):
    """
    本函数把一个 dict 或者 list 写入文件
    data 是 dict 或者 list
    path 是保存文件的路径
    """
    # json 是是个序列化/反序列化 list/dict 的库
    # indent 是缩进
    # ensure_ascii=False 用于保存路径
    s = json.dumps(data, indent=2, ensure_ascii=False)
    with open(path, 'w+', encoding='utf-8') as f:
        log('save', path, s, data)
        f.write(s)


def load(path):
    """
    本函数从一个文件中载入数据并转化为 dict 或者 list
    path 是保存文件的路径
    """
    with open(path, 'r', encoding='utf-8') as f:
        s = f.read()
        log('load s', type(s), s)
        j = json.loads(s)
        log('load j', type(j), j)
        return j


class Model(object):
    # Model 是用于存储数据的基类
    # @classmethod 说明这是一个类方法
    # 类方法的调用方法是 类名。类方法（）
    @classmethod
    def db_path(cls):
        """
        cls 是类名，谁调用的类名就是谁的
        classmethod 有一个参数是 class（这里我们用 cls 这个名字）
        所以我们可以得到 class 的名字
        """
        classname = cls.__name__
        path = '{}.txt'.format(classname)
        return path

    @classmethod
    def new(cls, form):
        # cls(from) 相当于 User（form）
        m = cls(form)
        return m

    @classmethod
    def all(cls):
        """
        all 方法（类里面的函数叫方法）使用 load 函数得到所有的 models
        """
        path = cls.db_path()
        models = load(path)
        ms = [cls.new(m) for m in models]
        return ms

    def save(self):
        """
        用 all 方法读取文件中所有 model 并生成一个 list
        把 self 添加进去并且保存进文件
        """
        # self.__class__.all()
        models = self.all()
        log('models', models)
        # __dict__是包含了对象所有属性和值的字典
        data = [m.__dict__ for m in models]
        path = self.db_path()
        save(data, path)

    def __repr__(self):
        """
        __repr__是一个魔法方法
        简单来说，它的作用是得到类的 字符串表达形式
        """
        classname = self.__class__.__name__
        properties = [
            '{}: ({})'.format(k, v)for k, v in self.__dict__.items()
        ]
        s = '\n'.join(properties)
        return '< {}\n{} >\n'.format(classname, s)


class User(Model):
    def __init__(self, form):
        self.username = form.get('username', '')
        self.password = form.get('password', '')

    def validate_login(self):
        return self.username == 'gua' and self.password == '123'

    def validate_register(self):
        return len(self.username) > 2 and len(self.password) > 2

    
class Message(Model):
    def __init__(self, form):
        self.message = form.get('message', '')
        self.author = form.get('author', '')