from models import Model
from utils import log


class Weibo(Model):

    def __init__(self, form):
        super().__init__(form)
        self.title = form.get('title', '')
        self.user_id = form.get('user_id', -1)
        # self.weibo_id = form.get('weibo_id', -1)

    @classmethod
    def update(cls, form):
        weibo_id = int(form['id'])
        data = Weibo.find_by(id=weibo_id)
        data.title = form['title']
        data.save()

    @classmethod
    def add(cls, form, user_id):
        log('add_form', form)
        data = Weibo.new(form)
        data.user_id = user_id
        data.save()
