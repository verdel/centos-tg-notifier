import os
import logging


class DevelopmentConfig(object):
    MONGODB_DB = 'notifier'
    MONGODB_HOST = 'localhost'
    MONGODB_PORT = 27017
    MONGODB_USERNAME = ''
    MONGODB_PASSWORD = ''
    TG_TOKEN = ''
    TG_PROXY_URL = ''
    TG_PROXY_USER = ''
    TG_PROXY_PASS = ''
    LOGGING_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    LOGGING_LEVEL = logging.INFO


class ProductionConfig(object):
    MONGODB_DB = os.getenv('MONGODB_DB', 'notifier')
    MONGODB_HOST = os.getenv('MONGODB_HOST', 'localhost')
    MONGODB_PORT = os.getenv('MONGODB_PORT', 27017)
    MONGODB_USERNAME = os.getenv('MONGODB_USERNAME', '')
    MONGODB_PASSWORD = os.getenv('MONGODB_PASSWORD', '')
    TG_TOKEN = os.getenv('TG_TOKEN', '')
    TG_PROXY_URL = os.getenv('TG_PROXY_URL', '')
    TG_PROXY_USER = os.getenv('TG_PROXY_USER', '')
    TG_PROXY_PASS = os.getenv('TG_PROXY_PASS', '')

    LOGGING_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    LOGGING_LEVEL = logging.INFO


config = {
    "development": "DevelopmentConfig",
    "production": "ProductionConfig",
    "default": "ProductionConfig"
}


def configure_app():
    config_name = os.getenv('REGISTRATOR_CONFIGURATION', 'default')
    return globals()[config[config_name]]()
