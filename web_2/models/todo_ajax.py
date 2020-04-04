from time import time

from models.base_model import  SQLModel


class TodoAjax(SQLModel):
    sql_create = '''
        CREATE TABLE `todoajax` (
            `id`        INT NOT NULL AUTO_INCREMENT,
            `title`     VARCHAR(255) NOT NULL,
            `user_id`   INT NOT NULL,
            PRIMARY KEY (`id`)
        );
        '''

    def __init__(self, form):
        super().__init__(form)
        self.title = form.get('title', '')

        self.user_id = form.get('user_id', None)

    @classmethod
    def add(cls, form, user_id):
        t = cls(form)
        t.user_id = user_id
        _id = t.insert(t.__dict__)
        t.id = _id
        return t