import socket
import urllib.parse

# import threading
import _thread

from utils import log

from routes import error
from routes import route_dict


# define a Class for restoring request data
class Request(object):
    def __init__(self, r):
        self.raw_data = ''
        self.method = 'GET'
        self.path = ''
        self.query = {}
        self.body = ''
        self.headers = {}
        self.cookies = {}

        self.raw_data = r
        # put the body into request
        header, self.body = r.split('\r\n\r\n', 1)
        h = header.split('\r\n')
        # log('heads', h)
        parts = h[0].split()
        self.path = parts[1]
        self.method = parts[0]
        self.heads = parts[1:]
        self.add_headers(h[1:])

        # self.path, self.query = parsed_path(self.path)
        # log('path and query', self.path, self.query)

    def add_headers(self, header):

        lines = header
        for line in lines:
            k, v = line.split(':', 1)
            self.headers[k] = v

        if 'Cookie' in self.headers:
            cookies = self.headers['Cookie'].split(';')
            log('original cookies', cookies)
            for cookie in cookies:
                k, v = cookie.split('=')
                self.cookies[k] = v

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
    if index == -1:
        return path, {}
    else:
        p = path[:index]
        query_string = path[index + 1:]
        args = query_string.split('&')
        query = {}
        for arg in args:
            k, v = arg.split('=')
            query[k] = v
        return p, query


def request_from_connection(connection):
    request = b''
    buffer_size = 1024
    while True:
        r = connection.recv(buffer_size)
        request += r
        if len(r) < buffer_size:
            request = request.decode()
            log('request\n {}'.format(request))
            return request


def response_for_request(request):
    """
    rely on what path get function
    if do not find report 404
    """
    request.path, request.query = parsed_path(request.path)
    r = route_dict()
    response = r.get(request.path, error)
    return response(request)


def process_connection(connection):
    with connection:
        # log('haha connection', connection)
        r = request_from_connection(connection)
        if len(r) > 0:
            request = Request(r)
            response = response_for_request(request)
            connection.sendall(response)
        else:
            connection.sendall(b'')
            log('accept a empty request')


def run(host, port):
    """
    start sever
    """
    log('start running', 'http://{}:{}'.format(host, port))
    with socket.socket() as s:
        s.bind((host, port))

        s.listen()
        while True:
            connection, address = s.accept()
            log('ip <{}>\n'.format(address))
            _thread.start_new_thread(process_connection, (connection,))

            # t = threading.Thread(target=process_connection, args=(connection,))
            # t.start()

            # with connection:
            #     r = request_from_connection(connection)
            #     if len(r) > 0:
            #         request = Request(r)
            #         response = response_for_request(request)
            #         connection.sendall(response)
            #     else:
            #         connection.sendall(b'')
            #         log('accept a empty')


if __name__ == '__main__':
    config = dict(
        host='localhost',
        port=3000,
    )
    run(**config)