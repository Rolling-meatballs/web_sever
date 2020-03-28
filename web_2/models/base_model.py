import pymysql

import random
from utils import (
    log,
    random_string
)
import time

import config
import secret


class SQLModel(object):
    connection = None

    @classmethod
    def init_db(cls):
        cls.connection = pymysql.connect(
            host='localhost',
            user='root',
            password=secret.mysql_password,
            db=config.db_name,
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )

    def __init__(self, form):
        self.id = form.get('id', None)

    @classmethod
    def table_name(cls):
        return '`{}`'.format(cls.__name__)

    @classmethod
    def new(cls, form):
        m = cls(form)
        id = cls.insert(m.__dict__)
        m.id = id
        return m

    @classmethod
    def insert(cls, form):
        form.pop('id')
        sql_keys = ', '.join(['`{}`'.format(k) for k in form.keys()])
        sql_values = ', '.join(['%s'] * len(form))
        sql_insert = 'INSERT INTO {} ({}) VALUES ({})'.format(
            cls.table_name(),
            sql_keys,
            sql_values,
        )
        log('ORM insert <{}>'.format(sql_insert))

        values = tuple(form.values())

        with cls.connection.cursor() as cursor:
            cursor.execute(sql_insert, values)
            _id = cursor.lastrowid
        cls.connection.commit()

        return _id

    @classmethod
    def delete(cls, id):
        sql_delete = 'DELETE FROM {} WHERE `id`=%s'.format(cls.table_name())
        log('ORM delete <{}>'.format(sql_delete.replace('\n', ' ')))

        with cls.connection.cursor() as cursor:
            cursor.execute(sql_delete, (id))
        cls.connection.commit()

    @classmethod
    def update(cls, id, **kwargs):
        # UPDATE

        sql_set = ', '.join(
            ['`{}`=%s'.format(k) for k in kwargs.keys()]
        )
        sql_update = 'UPDATE {} SET {} WHERE `id`=%s'.format(
            cls.table_name(),
            sql_set,
        )
        log('ORM update <{}>'.format(sql_update.replace('\n', ' ')))

        values = list(kwargs.values())
        values.append(id)
        values = tuple(values)

        with cls.connection.cursor() as cursor:
            cursor.execute(sql_update, values)
        cls.connection.commit()

    @classmethod
    def one(cls, **kwargs):
        log('kwargs', kwargs)
        sql_set = 'AND '.join(
            ['`{}`= %s'.format(k) for k in kwargs.keys()]
        )
        sql = 'SELECT * FROM {} WHERE {}'.format(
            cls.table_name(),
            sql_set,
        )
        log('sql', sql)

        values = list(kwargs.values())
        log('values:', values)
        values = tuple(values)
        log('values2', values)

        with cls.connection.cursor() as cursor:
            s = cursor.execute(sql, (values,))
            log('one_test', s)
            result = cursor.fetchone()
            log('result', result)

        if result is None:
            return None
        else:
            m = cls(result)
            return m

    @classmethod
    def all(cls, **kwargs):
        log('kwargs', kwargs)
        sql_set = 'AND '.join(
            ['`{}`=%s '.format(k) for k in kwargs.keys()]
        )
        if len(kwargs) > 0:
            sql = 'SELECT * FROM {} WHERE {}'.format(
                cls.table_name(),
                sql_set,
            )

            log('sql', sql)

            values = list(kwargs.values())
            log('values:', values)
            values = tuple(values)
            log('values2:', values)

            with cls.connection.cursor() as cursor:
                s = cursor.execute(sql, (values,))
                log('all_test:', s)
                result = cursor.fetchall()
                log('result', result)

        else:
            sql = 'SELECT * FROM {}'.format(
                cls.table_name(),
            )
            with cls.connection.cursor() as cursor:
                s = cursor.execute(sql)
                log('all_test', s)
                result = cursor.fetchall()
                log('result', result)

        if result is None:
            return None
        else:
            ms = []
            for m in result:
                ms.append(cls(m))
                log('ms', ms)
            return ms

    def __repr__(self):

        name = self.__class__.__name__
        properties = ['{}: ({})'. format(k, v) for k, v in self.__dict__.items()]
        s = '\n'.join(properties)
        return '< {}\n{} >\n'.format(name, s)

    def json(self):
        return self.__dict__

# def main():
#     SessionSQL.save('3')
#
#
# if __name__ == '__main__':
#     main()
