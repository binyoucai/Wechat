import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

IMAGE_DIR = os.path.join(BASE_DIR, 'App/views/ext_api_tool/images')
FACE_DIR = os.path.join(BASE_DIR, 'App/views/ext_api_tool/faces')
FONTLIB_DIR = os.path.join(BASE_DIR, 'App/views/ext_api_tool/fontlib')

# 图灵
TULING_API_KEY = 'ef1b770c6b044cd787701e13929c563b'
TULING_UER_ID = 'python'

# 腾讯人脸识别
TENCENT_APP_ID = '1106860829'
TENCENT_APP_KEY = 'P8Gt8nxi6k8vLKbS'

# 微信公众号配置
WX_TOKEN = ''
WX_APP_ID = ''
WX_SECRET_KEY = ''


def get_db_uri(dbinfo):
    engine = dbinfo.get("ENGINE") or "sqlite"
    driver = dbinfo.get("DRIVER") or "sqlite"
    user = dbinfo.get("USER") or ""
    password = dbinfo.get("PASSWORD") or ""
    host = dbinfo.get("HOST") or ""
    port = dbinfo.get("PORT") or ""
    name = dbinfo.get("NAME") or ""

    return "{}+{}://{}:{}@{}:{}/{}".format(engine, driver, user, password, host, port, name)


class Config:
    DEBUG = False

    TESTING = False

    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopConfig(Config):
    DEBUG = True

    dbinfo = {

        "ENGINE": "mysql",
        "DRIVER": "pymysql",
        "USER": "",
        "PASSWORD": "",
        "HOST": "localhost",
        "PORT": "3306",
        "NAME": ""

    }

    SQLALCHEMY_DATABASE_URI = get_db_uri(dbinfo)


class TestConfig(Config):
    TESTING = True

    dbinfo = {

        "ENGINE": "mysql",
        "DRIVER": "pymysql",
        "USER": "",
        "PASSWORD": "",
        "HOST": "localhost",
        "PORT": "3306",
        "NAME": ""

    }

    SQLALCHEMY_DATABASE_URI = get_db_uri(dbinfo)


class StagingConfig(Config):
    dbinfo = {

        "ENGINE": "mysql",
        "DRIVER": "pymysql",
        "USER": "",
        "PASSWORD": "",
        "HOST": "localhost",
        "PORT": "3306",
        "NAME": ""

    }

    SQLALCHEMY_DATABASE_URI = get_db_uri(dbinfo)


class ProductConfig(Config):
    dbinfo = {

        "ENGINE": "mysql",
        "DRIVER": "pymysql",
        "USER": "root",
        "PASSWORD": "",
        "HOST": "localhost",
        "PORT": "3306",
        "NAME": ""

    }

    SQLALCHEMY_DATABASE_URI = get_db_uri(dbinfo)


envs = {
    "develop": DevelopConfig,
    "testing": TestConfig,
    "staging": StagingConfig,
    "product": ProductConfig,
    "default": DevelopConfig
}
