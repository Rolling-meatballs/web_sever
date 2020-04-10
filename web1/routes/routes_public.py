from flask import (
    Blueprint,
    render_template,
)

from routes import (
    current_user,
)
from utils import log


bp = Blueprint('public',__name__)


@bp.route('/')
def index():
    """
    主页的处理函数, 返回主页的响应
    """
    u = current_user()
    return render_template('index.html', username=u.username)


# def static(request):
#     """
#     静态资源的处理函数, 读取图片并生成响应返回
#     """
#     filename = request.query.get('file', 'doge.gif')
#     path = 'static/' + filename
#     with open(path, 'rb') as f:
#         # header = b'HTTP/1.x 200 OK\r\nContent-Type: image/gif\r\n\r\n'
#         header = b'HTTP/1.x 200 OK\r\n\r\n'
#         img = header + f.read()
#         return img


def route_dict():
    """
    路由字典
    key 是路由(路由就是 path)
    value 是路由处理函数(就是响应)
    """
    d = {
        '/': index,
    }
    return d
