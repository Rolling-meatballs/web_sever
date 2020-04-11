from routes.routes_todo import route_dict as todo_routes
from routes.routes_weibo import route_dict as weibo_routes
from routes.routes_user import route_dict as user_routes
from routes.routes_public import route_dict as public_routes
from web_framework import url_map, response_for_path


def configured_application():
    url_map.update(todo_routes())
    url_map.update(weibo_routes())
    url_map.update(user_routes())
    url_map.update(public_routes())

    def app(request):
        return response_for_path(request)

    return app
