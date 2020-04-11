from utils import log
from app import configured_application
application = configured_application()
log('wsgi loading succeed')