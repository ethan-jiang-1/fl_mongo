from flask import Flask
from .config import config, APP_VERSION


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

    return app


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