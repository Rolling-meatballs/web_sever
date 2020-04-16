from sqlalchemy import create_engine

import secret
from config import db_name
from app import  configured_app
from models.base_model import db
from models.user import User
from models.topic import Topic
from models.reply import Reply


def reset_database():
    # now mysql root approve of pass by socket but password
    url = 'mysql+pymysql://root:{}@localhost/?charset=utf8mb4'.format(
        secret.mysql_password
    )
    e = create_engine(url, echo=True)

    with e.connect() as c:
        c.execute('DROP DATABASE IF EXISTS {}'.format(db_name))
        c.execute('CREATE DATABASE {} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci'.format(db_name))
        c.execute('USE {}'.format(db_name))

    db.metadata.create_all(bind=e)

def generate_fake_data():
    form = dict(
        username='gua',
        password='123',
    )
    u = User.register(form)

    with open('markdown_demo.md', encoding='utf8') as f:
        content = f.read()
    form = dict(
        title='markdown demo',
        content=content,
    )
    Topic.add(form, u.id)


if __name__ == '__main__':
    app = configured_app()
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.config['SEND_FILE_MAX _AGE_DEFAULT'] = 0
    with app.app_context():
        reset_database()
        generate_fake_data()