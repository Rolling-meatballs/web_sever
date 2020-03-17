from jinja2 import (
    Environment,
    FileSystemLoader,
)

import os.path

from utils import log


path = os.path.join(os.path.dirname(__file__), 'templates')
log('test path', __file__, os.path.dirname(__file__), path)

loader = FileSystemLoader(path)

e = Environment(loader=loader)

template = e.get_template('demo.html')

ns = range(3)
us = [
    {
        'id': 1,
        'name': 'gua',
    },
    {
        'id': 2,
        'name': '瓜'
    },
]
log(template.render(
    name='gua', numbers=ns, users=us
))