from models.base_model import SQLModel


class userajax(SQLModel):
    sql_create = '''
        CREATE TABLE `user_ajax` (
        `id`        INT NOT NULL  AUTO_INCREMENT,
        `username`  VARCHAR(255) NOT NULL,
        
    '''
    super().__init__()