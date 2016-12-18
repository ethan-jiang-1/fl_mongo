from flask import Flask
from .config import config, APP_VERSION
from .extensions import mongo, mdb


# flask app for main
def create_app(config_name, app_config_extra=None):
    # the flask application
    app = Flask("app")
    app.VERSION = APP_VERSION

    app_config = app_init_config(app, config, config_name, app_config_extra)
    if app_config is None:
        return None

    # init application config
    app.config.from_object(app_config)

    mongo.init_app(app)
    mdb.init_app(app)

    app_add_blueprints(app)

    return app


# add all blueprints 
def app_add_blueprints(app):
    from app.pages_root.views import add_blueprint_pages_root
    add_blueprint_pages_root(app)

    from app.pages_exam_db.views import add_blueprint_pages_exam_db
    add_blueprint_pages_exam_db(app)

    from app.pages_exam_mdb.views import add_blueprint_pages_exam_mdb
    add_blueprint_pages_exam_mdb(app)

    from app.pages_exam_mix.views import add_blueprint_pages_exam_mix
    add_blueprint_pages_exam_mix(app)


# init app configurateion - factory mode
def app_init_config(app, config, config_name, app_config_extra):

    if config_name is None:
        config_name = "default"
    if config_name not in config:
        print("Error: config not found: " + str(config_name))
        return None

    # select the app_config
    app_config = config[config_name]

    # add config from app_config_extra
    if app_config_extra is not None:
        for name in app_config_extra:
            setattr(app_config, name, app_config_extra[name])

    # init app_config
    app_config.init_app(app)

    return app_config    