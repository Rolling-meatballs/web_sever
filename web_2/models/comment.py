from models import Model
from utils import log
# from models.weibo import Weibo


class Comment(Model):

    def __init__(self, form, user_id=-1):
        super().__init__(form)
        self.content = form.get('content', '')
        self.weibo_id = int(form.get('weibo_id', -1))
        self.user_id = form.get('user_id', user_id)

    @classmethod
    def update(cls, form):
        log('add_form', form)
        comment_id = int(form['id'])
        # weibo_id = Weibo.id
        w = Comment.find_by(id=comment_id)
        w.content =form['content']
        w.save()

    def user(self):
        u = User.find_by(id=self.user_id)
        return u
