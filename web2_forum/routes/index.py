from flask import (
    request,
    url_for,
    Blueprint,
    render_template,
)

from utils import log


main = Blueprint('index', __name__)


@main.route('/')
def index():
    return render_template('index.html')


@main.route('/register', methods=['POST'])
def register():
    pass


@main.route('/login', methods=['POST'])
def login():
    pass