from models import Model


class Message(Model):
    """
    Massage 是用来保存留言的 model
    """
    def __init__(self, form):
        super().__init__(form)
        self.message = form.get('message', '')
        self.author = form.get('author', '')