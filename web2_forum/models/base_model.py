import time

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import (
    Column,
    Integer,
    String,
)
from sqlalchemy.orm import Query

from utils import log

db = SQLAlchemy()


def utctime():
    return int(time.time())


class SQLMixin(object):
    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True )
    created_time = Column(Integer, default=utctime)
    updated_time = Column(Integer, default=utctime)

    @classmethod
    def new(cls, form):
        m = cls()
        for name , value in form.items():
            setattr(m, name, value)

        m.save()
        # db.session.add(m)
        # db.session.commit()

        return m

    @classmethod
    def delete(cls, id):
        cls.query.filter_by(id=id).delete()
        db.session.commit()

    @classmethod
    def update(cls, id, **kwargs):
        m = cls.query.filter_by(id=id).first()
        for name, value in kwargs.items():
            setattr(m, name, value)
        m.save()
        # db.session.add(m)
        # db.session.commit()

    @classmethod
    def all(cls, **kwargs):
        ms = cls.query.filter_by(**kwargs).all()
        return ms

    @classmethod
    def one(cls, **kwargs):
        ms = cls.query.filter_by(**kwargs).first()
        return ms

    @classmethod
    def colums(cls):
        return cls.__mapper__.c.items()

    def __repr__(self):
        """
        get the class as a str form
        :return:
        """
        classname = self.__class__.__name__
        properties = ['{}: ({})'.format(k, v) for k, v in self.__dict__.items()]
        s = '\n'.join(properties)
        return '< {}\n{} \n>\n'.format(classname, s)

    def save(self):
        # log('save db', db.session)
        # log('save self', self)
        db.session.add(self)
        db.session.commit()


# class SimpleUser(SQLMixin, db.Model):
#     # username: str
#     username = Column(String(50), nullable=False)
#     password = Column(String(50), nullable=False)
#
#     # def __init__(self):
#     #     self.username = form.get('username', 'guest')
#     #     self.password = 'xxx'
#
#
# if __name__ == '__main__':
#     db.create_all()
#     form = dict(
#         username='123',
#         password='456',
#     )
#     u = SimpleUser.new(form)
#     print(u)
#     u = SimpleUser.one(username='123')
#     print(u)

