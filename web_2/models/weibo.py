from models import Model
from models.comment import Comment
from models.base_model import SQLModel


class Weibo(SQLModel):
    """
    微博类
    """
    def __init__(self, form):
        super().__init__(form)
        self.content = form.get('content', '')
        # 和别的数据关联的方式, 用 user_id 表明拥有它的 user 实例
        self.user_id = form.get('user_id', None)

    @classmethod
    def add(cls, form, user_id):
        w = Weibo(form)
        w.user_id = user_id
        w.new(w)

    @classmethod
    def update(cls, form):
        weibo_id = int(form['id'])
        w = Weibo.one(id=weibo_id)
        w.title = form['content']
        w.save()

    def comments(self):
        cs = Comment.all(weibo_id=self.id)
        return cs