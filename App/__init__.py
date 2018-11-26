from flask import Flask

from App.ext import init_ext
from App.settings import envs
from App.views import init_view


def create_app(env):
    app = Flask(__name__)

    app.config.from_object(envs.get(env)) # 读取配置文件

    init_ext(app) # 初始化第三方插件

    init_view(app=app) # 注册视图函数

    return app