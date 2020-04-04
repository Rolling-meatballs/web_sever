import pymysql

import secret
import config
from models.base_model import SQLModel
from models.test_model import Test
from models.session import Session
from models.user_role import UserRole
from models.user import User
from models.todo_ajax import TodoAjax
# from models.comment import Comment
from models.weibo import Weibo
from models.comment import Comment
from utils import log


def recreate_table(cursor):
    cursor.execute(Test.sql_create)
    cursor.execute(User.sql_create)
    cursor.execute(Session.sql_create)
    cursor.execute(TodoAjax.sql_create)
    # cursor.execute(Weibo.sql_create)
    # cursor.execute(Comment.sql_create)


def recreate_database():
    connection = pymysql.connect(
        host='localhost',
        user='root',
        password=secret.mysql_password,
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )
    try:
        with connection.cursor() as cursor:
            cursor.execute(
                'DROP DATABASE IF EXISTS `{}`'.format(
                    config.db_name
                )
            )
            cursor.execute(
                'CREATE DATABASE `{}` DEFAULT CHARACTER SET utf8mb4'.format(
                    config.db_name
                )
            )
            cursor.execute('USE `{}`'.format(config.db_name))

            recreate_table(cursor)

        connection.commit()
    finally:
        connection.close()

def test_one():
    User.init_db()
    User.one(username='ddd', )
    User.one( password='1234', )
    User.one(username='ddd', password='1234', )


def test_all():
    User.init_db()
    User.all()
    User.all(username='ddd', )
    User.all( password='1234', )
    # User.all(username='ddd', password='1234', )




def fake_data():
    SQLModel.init_db()

    Test.new({})

    form = dict(
        username='gua',
        password='123',
        role=UserRole.normal,
    )
    u, result = User.register(form)

    Session.add(u.id)

    form = dict(
        title='test todo ajax',
    )
    t = TodoAjax.add(form, u.id)

    # form = dict(
    #     content='test weibo',
    # )
    # w = Weibo.add(form, u.id)
    # form = dict(
    #     content='test comment',
    #     weibo_id=w.id,
    # )
    # Weibo.comment_add(form, u.id)
    #
    # SQLModel.connection.close()



if __name__ == '__main__':
    # recreate_database()
    fake_data()
    # test_one()
    # test_all()