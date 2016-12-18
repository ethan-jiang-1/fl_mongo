from flask import Blueprint

pages_exam_db = Blueprint('pages_exam_db', __name__, url_prefix='/exam_db')


@pages_exam_db.route('/', methods=["GET"])
def exam_index():
    return "exam_index"


def add_blueprint_pages_exam_db(app):
    app.register_blueprint(pages_exam_db)
    return pages_exam_db
