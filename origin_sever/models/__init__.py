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
    def __int__(self, form):
        self.id = form.get('id', None)

    @classmethod
    def db_path(cls):
        """
        cls 是类名，谁调用的类名就是谁的
        classmethod 有一个参数是 class（这里我们用 cls 这个名字）
        所以我们可以得到 class 的名字
        """
        classname = cls.__name__
        path = 'db/{}.txt'.format(classname)
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

    @classmethod
    def find_by(cls, **kwargs):
        log('find_by kwargs', kwargs)

        for m in cls.all():
            exist = True
            for k, v in kwargs.items():
                if not hasattr(m, k) or not getattr(m, k) == v:
                    exist = False
                    log('exist', m, k)
                    break
            if exist:
                return m

    @classmethod
    def find_all(cls, **kwargs):
        log('find_all_kwargs', kwargs)
        models = []

        for m in cls.all():
            exist = True
            for k, v in kwargs.items():
                if not hasattr(m, k) or not getattr(m, k) == v:
                    exist = False
                    break
            if exist:
                models.append(m)

        return models

    def insert(self, models):
        log('添加数据', models)

        if len(models) > 0:
            log('model length', models[-1], models)
            self.id = models[-1].id + 1
        else:
            log('frist model', self.id)
            self.id = 1
        models.append(self)

    def update(self, models):
        log('更新数据')
        # 有 id 说明已经是存在于数据文件中的数据
        # 那么就找到这条数据并替换
        for i, m in enumerate(models):
            if m.id == self.id:
                models[i] = self
                break

    def save(self):
        """
        用 all 方法读取文件中所有 model 并生成一个 list
        把 self 添加进去并且保存进文件
        """
        # self.__class__.all()
        models = self.all()
        log('models', models)
        # __dict__是包含了对象所有属性和值的字典
        # data = [m.__dict__ for m in models]
        # path = self.db_path()
        # save(data, path)
        if self.id is None:
            self.insert(models)
        else:
            self.update(models)

        log('save data', self.id)
        #保存
        #__dict__ 是包含了对象所有属性和值的字典
        l = [m.__dict__ for m in models]
        path = self.db_path()
        save(l, path)

    def __repr__(self):
        """
        __repr__是一个魔法方法
        简单来说，它的作用是得到类的 字符串表达形式
        """
        classname = self.__class__.__name__
        properties = [
            '{}: ({})'.format(k, v) for k, v in self.__dict__.items()
        ]
        s = '\n'.join(properties)
        return '< {}\n{} >\n'.format(classname, s)
