import time

from flask import Flask
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

import config
import secret

from models.base_model import db
from models.board import Board
from models.user import User
from models.topic import Topic
from models.reply import Reply

from routes import index
from utils import log

from routes.index import main as index_routes
from routes.index import main as not_found
from routes.topic import main as topic_routes
from routes.reply import main as reply_routes


class UserModelView(ModelView):
    column_searchable_list = ('username', 'password')


def remove_script(content: str):
    log('remove_script <{}>'.format(content))
    c = content
    c = c.replace('>', '&gt')
    c = c.replace('>', '&lt')
    c = c.replace('script', 'removed')
    log('remove_script after <{}>'.format(c))
    return c


def format_time(unix_timestamp):
    f = '%Y-%m-%d %H:%M:%S'
    value = time.localtime(int(unix_timestamp))
    formatted = time.strftime(f, value)
    return formatted


def current_time():
    time_format = '%Y/%m/%d %H:%M:%S'
    localtime = time.localtime(int(time.time()))
    formatted = time.strftime(time_format, localtime)
    return dict(current_time=formatted)


def configured_app():
    db_name = config.db_name
    app = Flask(__name__)
    # set secret_key for flask session
    app.secret_key = secret.secret_key
    # data return order
    #mysql -> pymysql -> sqlalchemy -> route
    #initialization order
    #app -> flask-sqlalchemy -> sqlalchemy -> pymysql -> mysql

    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:{}@localhost/{}?charset=utf8mb4'.format(
        secret.mysql_password,
        db_name,
    )
    db.init_app(app)

    app.template_filter()(remove_script)
    # app.context_processor(current_time)
    app.template_filter()(format_time)
    # app.errorhandler(404)(not_found)

    admin = Admin(app, name=db_name, template_mode='bootstrap3')
    mv = UserModelView(User, db.session)
    admin.add_view(mv)
    mv = ModelView(Board, db.session)
    admin.add_view(mv)

    register_routes(app)
    return app


def register_routes(app):
    app.register_blueprint(index_routes)
    app.register_blueprint(topic_routes, url_prefix='/topic')
    app.register_blueprint(reply_routes, url_prefix='/reply')
    # log('url map', app.url_map)

#run
if __name__ == '__main__':
    app = configured_app()
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    # app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    app.jinja_env.auto_reload = True
    app.config['SEND_FILE_MAX _AGE_DEFAULT'] = 0
    config = dict(
        debug=True,
        host='localhost',
        port=3000,
    )
    app.run(**config)