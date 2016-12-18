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

    MONGO_URI = "mongodb://localhost:27017/pym_base"

    MONGODB_DB = 'mdb_base'
    MONGODB_HOST = "localhost"
    MONGODB_PORT = 27017
    # MONGODB_USERNAME
    # MONGODB_PASSWORD

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(BaseConfig):
    APP_RUNNING_MODE = "development"

    DEBUG = True
    TESTING = False

    MONGO_URI = "mongodb://localhost:27017/pym_development"

    MONGODB_DB = 'mdb_development'
    MONGODB_HOST = "localhost"
    MONGODB_PORT = 27017

    @staticmethod
    def init_app(app):
        pass


class StagingConfig(BaseConfig):
    APP_RUNNING_MODE = "production"

    DEBUG = False
    TESTING = False

    SERVER_NAME = "test.mysite.com"

    MONGO_URI = "mongodb://localhost:27017/pym_staging"

    MONGODB_DB = 'mdb_staging'
    MONGODB_HOST = "localhost"
    MONGODB_PORT = 27017

    @staticmethod
    def init_app(app):
        pass


class ProductionConfig(BaseConfig):
    APP_RUNNING_MODE = "production"

    DEBUG = False
    TESTING = False

    SERVER_NAME = "production.mysite.com"

    MONGO_URI = "mongodb://localhost:27017/pym_production"

    MONGODB_DB = 'mdb_production'
    MONGODB_HOST = "localhost"
    MONGODB_PORT = 27017

    @staticmethod
    def init_app(app):
        pass


class TestConfig(BaseConfig):
    APP_RUNNING_MODE = "test"

    DEBUG = True
    TESTING = True

    SERVER_NAME = "test.mysite.com"

    MONGO_URI = "mongodb://localhost:27017/pym_test"

    MONGODB_DB = 'mdb_test'
    MONGODB_HOST = "localhost"
    MONGODB_PORT = 27017

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