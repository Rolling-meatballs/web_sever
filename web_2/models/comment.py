from models import Model
from utils import log
from models.weibo import Weibo


class Comment(Model):
    def __init__(self, form):
        super().__init__(form)
        self.title = form.get('comment_title', '')
        self.comment_id = form.get('comment_id', -1)
        self.weibo_id = form.get('weibo_id', -1)
        self.user_id = form.get('user_id', -1)

    @classmethod
    def add(cls, form, user_id, weibo_id):
        log('add_form', form)
        data = Comment.new(form)
        # weibo_id = Weibo.id
        data.comment_title = form['comment_title']
        data.weibo_id = weibo_id
        data.user_id = user_id
        data.save()