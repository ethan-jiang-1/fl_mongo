from flask import Blueprint

pages_exam_mix = Blueprint('pages_exam_mix', __name__, url_prefix='/exam_mix')


@pages_exam_mix.route('/', methods=["GET"])
def exam_mix_index():
    return "exam_mix_index"


def add_blueprint_pages_exam_mix(app):
    app.register_blueprint(pages_exam_mix)
    return pages_exam_mix
