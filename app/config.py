# -*- coding: utf-8 -*-
import os


_basedir = os.path.abspath(os.path.dirname(__file__))
APP_VERSION = "fl_mongo-0.0.1"


class BaseConfig(object):
    # App Default Setting, global/env setting
    APP_RUNNING_MODE = ""

    DEBUG = False
    TESTING = False

    SECRET_KEY = os.environ.get('SECRET_KEY') or 'BoWh3@D'

    APP_ROOT_DIR = _basedir                            # the root of the app
    PRJ_ROOT_DIR = os.path.normpath(_basedir + "/..")  # the root of the project


    MONGO_URI = "mongodb://localhost:27017/fm_base"

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(BaseConfig):
    APP_RUNNING_MODE = "development"

    DEBUG = True
    TESTING = False

    MONGO_URI = "mongodb://localhost:27017/fm_development"

    @staticmethod
    def init_app(app):
        pass


class StagingConfig(BaseConfig):
    APP_RUNNING_MODE = "production"

    DEBUG = False
    TESTING = False

    SERVER_NAME = "test.mysite.com"

    MONGO_URI = "mongodb://localhost:27017/fm_staging"

    @staticmethod
    def init_app(app):
        pass


class ProductionConfig(BaseConfig):
    APP_RUNNING_MODE = "production"

    DEBUG = False
    TESTING = False

    SERVER_NAME = "production.mysite.com"

    MONGO_URI = "mongodb://localhost:27017/fm_production"

    @staticmethod
    def init_app(app):
        pass


class TestConfig(BaseConfig):
    APP_RUNNING_MODE = "test"

    DEBUG = True
    TESTING = True

    SERVER_NAME = "test.mysite.com"

    MONGO_URI = "mongodb://localhost:27017/fm_test"


    @staticmethod
    def init_app(app):
        pass


config = {
    'development': DevelopmentConfig,
    'staging': StagingConfig,
    'production': ProductionConfig,
    'test': TestConfig,
    'default': DevelopmentConfig,
}