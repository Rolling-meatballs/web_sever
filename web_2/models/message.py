from utils import log

from models import Model


class Message(Model):
    def __init__(self, form):
        self.message = form.get('message', '')
        self.author = form.get('author', '')