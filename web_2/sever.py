import socket
# import threading
import _thread

from utils import log

from request import Request
from routes import error

from routes.routes_todo import route_dict as todo_routes
from routes.routes_user import route_dict as user_routes
from routes.routes_public import route_dict as public_routes
from routes.routes_weibo import route_dict as weibo_routes


# def parsed_path(path):
#     index = path.find('?')
#     if index == -1:
#         return path, {}
#     else:
#         p = path[:index]
#         query_string = path[index + 1:]
#         args = query_string.split('&')
#         query = {}
#         for arg in args:
#             k, v = arg.split('=')
#             query[k] = v
#         return p, query


def response_for_path(request):
    r = {}
    r.update(todo_routes())
    r.update(user_routes())
    r.update(public_routes())
    r.update(weibo_routes())
    response = r.get(request.path, error) 
    return response(request)


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


def process_request(connection):
    r = request_from_connection(connection)

    request = Request(r)

    response = response_for_path(request)

    connection.sendall(response)


# def response_for_request(request):
#     """
#     rely on what path get function
#     if do not find report 404
#     """
#     request.path, request.query = parsed_path(request.path)
#     r = route_dict()
#     response = r.get(request.path, error)
#     return response(request)


# def process_connection(connection):
#     with connection:
#         # log('haha connection', connection)
#         # r = request_from_connection(connection)
#         r = connection.recv(1024)
#         r = r.decode()
#         log('http request\n{}'.format(r))
#         if len(r) > 0:
#             request = Request(r)
#             response = response_for_path(request)
#             log('http response\n{}'.format(response))
#             connection.sendall(response)
#         else:
#             # connection.sendall(b'')
#             log('accept a empty request')


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
            _thread.start_new_thread(process_request, (connection,))

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
        host='127.0.0.1',
        port=3000,
    )
    run(**config)