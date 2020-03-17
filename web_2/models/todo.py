from models import Model
from utils import log

import time


class Todo(Model):

    def __init__(self, form):
        super().__init__(form)
        self.title = form.get('title', '')
        self.user_id = form.get('user_id', -1)
        self.created_time = form.get('created_time', '')
        self.updated_time = form.get('updated_time', None)

    @classmethod
    def update(cls, form):
        log('updat_form', form)
        todo_id = int(form['user_id'])
        t = Todo.find_by(id=todo_id)
        t.title = form['title']
        t.save()

    @staticmethod
    def the_time():
        value = time.localtime(int(time.time()))
        time_format = '%Y/%m/%d %H:%M:%S'
        dt = time.strftime(time_format, value)
        return dt