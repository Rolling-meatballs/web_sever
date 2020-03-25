from models import Model
from models.comment import Comment
from utils import log


class Weibo(Model):

    def __init__(self, form):
        super().__init__(form)
        self.content = form.get('content', '')
        self.user_id = form.get('user_id', None)
        # self.weibo_id = form.get('weibo_id', -1)

    @classmethod
    def update(cls, form):
        weibo_id = int(form['id'])
        data = Weibo.find_by(id=weibo_id)
        data.title = form['content']
        data.save()

    @classmethod
    def add(cls, form, user_id):
        log('add_form', form)
        data = Weibo(form)
        data.user_id = user_id
        data.save()

    def comments(self):
        cs = Comment.find_all(weibo_id=self.id)
        return cs
