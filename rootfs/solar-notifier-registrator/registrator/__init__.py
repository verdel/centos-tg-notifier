# import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from mongoengine import connect
from registrator.config import configure_app
from registrator.commands import *


app_config = configure_app()
logging.basicConfig(
    format=app_config.LOGGING_FORMAT,
    level=app_config.LOGGING_LEVEL
)


def app():
    connect(
        db=app_config.MONGODB_DB,
        host=app_config.MONGODB_HOST,
        port=app_config.MONGODB_PORT,
        username=app_config.MONGODB_USERNAME,
        password=app_config.MONGODB_PASSWORD
    )

    if app_config.TG_PROXY_URL:
        REQUEST_KWARGS = {
            'proxy_url': app_config.TG_PROXY_URL,
            'urllib3_proxy_kwargs': {
                'username': app_config.TG_PROXY_USER,
                'password': app_config.TG_PROXY_PASS,
            }
        }
        updater = Updater(token=app_config.TG_TOKEN, use_context=True, request_kwargs=REQUEST_KWARGS)
    else:
        updater = Updater(token=app_config.TG_TOKEN)

    start_handler = CommandHandler('start', start, pass_args=True)
    stop_handler = CommandHandler('stop', stop)
    unknown_handler = MessageHandler(Filters.command, unknown)

    dp = updater.dispatcher
    dp.add_handler(start_handler)
    dp.add_handler(stop_handler)
    dp.add_handler(unknown_handler)

    updater.start_polling()
    updater.idle()
