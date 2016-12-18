def list_all_routes(the_app):
    """List all routes for the application"""
    import urllib
    from flask import url_for
    app = the_app
    output = []
    for rule in app.url_map.iter_rules():

        options = {}
        for arg in rule.arguments:
            options[arg] = "[{0}]".format(arg)

        methods = ','.join(rule.methods)
        url = url_for(rule.endpoint, **options)
        line = urllib.unquote("{:50s} {:26s} {}".format(rule.endpoint, methods, url))

        output.append(line)

    return output