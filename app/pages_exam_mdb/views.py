from flask import Blueprint

pages_exam_mdb = Blueprint('pages_exam_mdb', __name__, url_prefix='/exam_mdb')


@pages_exam_mdb.route('/', methods=["GET"])
def exam_mdb_index():
    return "exam_mdb_index"


def add_blueprint_pages_exam_mdb(app):
    app.register_blueprint(pages_exam_mdb)
    return pages_exam_mdb
