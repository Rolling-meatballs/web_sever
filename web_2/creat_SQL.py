import pymysql

import pymysql.connections
from utils import log

import secret
import config


def create(connection):
    sql_create_table = '''
    CREATE TABLE `session` (
        `id`            INT NOT NULL AUTO_INCREMENT,
        `session_id`    CHAR(255) NOT NULL,
        `user_id`       VARCHAR(255) NOT NULL,
        `created_time`  VARCHAR(255) NOT NULL,
        `expired`       VARCHAR(255) NOT NULL,
        PRIMARY KEY (`id`)
    );
    # CREATE UNIQUE INDEX session_id
    # on session (session_id);
    '''
    with connection.cursor() as cursor:
        cursor.execute(sql_create_table)
        log('setup succeed')


def main():
    connection = pymysql.connect(
        host='localhost',
        user='root',
        password=secret.mysql_password,
        db=config.db_name,
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )

    try:
        log('open the database')

        create(connection)
    finally:
        connection.close()


if __name__ == '__main__':
    main()