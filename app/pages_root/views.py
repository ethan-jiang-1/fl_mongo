from flask import Blueprint

pages_root = Blueprint('pages_root', __name__, url_prefix='')


@pages_root.route('/', methods=["GET"])
def root_index():
    return "root_index"


def add_blueprint_pages_root(app):
    app.register_blueprint(pages_root)
    return pages_root


