from app import configured_app
from utils import log

application = configured_app()
log('wsgi start')