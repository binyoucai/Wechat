from App.views.weixin_blue import weixin


def init_view(app):
    app.register_blueprint(blueprint=weixin)
