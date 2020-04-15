import time

from flask import Flask
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

import config

import secret

from routes import index
from utils import log

from routes.index import main as index_routes


def count(input):
    log('count using jinja filter')
    return len(input)


def format_time(unix_timestamp):
    f = '%Y-%m-%d %H:%M:%S'
    value = time.localtime(unix_timestamp)
    formatted = time.strftime(f, value)
    return formatted


def configured_app():
    db_name = config.db_name
    app = Flask(__name__)
    # set secret_key for flask session
    app.secret_key = config.secret_key
    # data return order
    #mysql -> pymysql -> sqlalchemy -> route
    #initialization order
    #app -> flask-sqlalchemy -> sqlalchemy -> pymysql -> mysql

    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:{}@localhost/{}?charset=utf8mb4'.format(
        secret.mysql_password,
        db_name,
    )


    app.register_blueprint(index_routes)

    app.template_filter()(count)
    app.template_filter()(format_time)

    # admin = Admin(app, name=db_name, template_mode='bootstrap3')

    return app

#run
if __name__ == '__main__':
    app = configured_app()
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.jinja_env.auto_reload = True
    app.config['SEND_FILE_MAX _AGE_DEFAULT'] = 0
    config = dict(
        debug=True,
        host='localhost',
        port=80,
    )
    app.run(**config)