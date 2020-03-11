import socket
import urllib.parse

import _thread

from utils import log

from routes import error
from  routes import route_dict

# define a Class for restoring request data
class Request(object):
    def __init__(self, r):
        self.raw_data = r
        # put the body into request
        header, self.body = r.split('\r\n\r\n', 1)
        h = header.split('\r\n')
        parts = h[0].split()
        self.path = parts[1]
        self.method = parts[0]

        self.path, self.query = parsed_path(self.path)
        log('path and query', self.path, self.query)

    def form(self):
        body = urllib.parse.unquote_plus(self.body)
        log('form', self.body)
        log('form', body)
        args = body.split('&')
        f = {}
        log('arg', args)
        for arg in args:
            k, v = arg.split('=')
            f[k] = v
        log('form() dictionary', f)
        return f


def parsed_path(path):
    index = path.find('?')