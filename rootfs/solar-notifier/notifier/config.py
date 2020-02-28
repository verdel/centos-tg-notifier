import os


class BaseConfig(object):
    DEBUG = False
    SECRET_KEY = '1d94e52c-1c89-4515-b87a-f48cf3cb7f0b'


class DevelopmentConfig(BaseConfig):
    DEBUG = True
    MONGODB_DB = 'notifier'
    MONGODB_HOST = 'localhost'
    MONGODB_PORT = 27017
    MONGODB_USERNAME = ''
    MONGODB_PASSWORD = ''
    SECRET_KEY = 'a9eec0e0-23b7-4788-9a92-318347b9a39f'
    ADMIN_NAME = 'admin'
    ADMIN_PASSWORD = 'test'
    TG_TOKEN = ''
    TG_PROXY_URL = ''
    TG_PROXY_USER = ''
    TG_PROXY_PASS = ''


class ProductionConfig(BaseConfig):
    DEBUG = False
    MONGODB_DB = os.getenv('MONGODB_DB', 'notifier')
    MONGODB_HOST = os.getenv('MONGODB_HOST', 'localhost')
    MONGODB_PORT = os.getenv('MONGODB_PORT', 27017)
    MONGODB_USERNAME = os.getenv('MONGODB_USERNAME', '')
    MONGODB_PASSWORD = os.getenv('MONGODB_PASSWORD', '')
    SECRET_KEY = 'a9eec0e0-23b7-4788-9a92-318347b9a39f'
    ADMIN_NAME = os.getenv('ADMIN_NAME', 'admin')
    ADMIN_PASSWORD = os.getenv('ADMIN_PASSWORD', 'admin')
    TG_TOKEN = os.getenv('TG_TOKEN', '')
    TG_PROXY_URL = os.getenv('TG_PROXY_URL', '')
    TG_PROXY_USER = os.getenv('TG_PROXY_USER', '')
    TG_PROXY_PASS = os.getenv('TG_PROXY_PASS', '')


config = {
    "development": "notifier.config.DevelopmentConfig",
    "production": "notifier.config.ProductionConfig",
    "default": "notifier.config.ProductionConfig"
}


def configure_app(app):
    config_name = os.getenv('NOTIFIER_CONFIGURATION', 'default')
    app.config.from_object(config[config_name])
    app.config.from_pyfile('config.cfg', silent=True)
