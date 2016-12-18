#!/usr/bin/env python
# encoding:utf8
from app.config import config
from app.main import create_app
from flask_script import Manager
from app.utils_manage.list_all_routes import list_all_routes


def create_app_for_manager(config_name=None, mulitple_app_mode=None):
    print "init app config name : %s" % config_name
    if config_name is not None:
        if config_name in config.keys():
            pass
        else:
            print "Wrong app config name: %s. Use default instead." % config_name
            config_name = 'default'
    else:
        config_name = 'default'

    print "active app config: %s\n" % config_name

    app = create_app(config_name, app_config_extra={})

    # migrate = Migrate(app, db)
    # app.migrate = migrate
    return app


# the manager
manager = Manager(create_app_for_manager)
manager.add_option('-c', '--config', help='config_name: development,test,production or default', dest='config_name', required=False)
# manager.add_command('db', MigrateCommand)


@manager.command
def list_routes():
    """List all routes for the application"""
    output = list_all_routes(manager.app)

    for line in sorted(output):
        print line


if __name__ == '__main__':
    manager.run()
