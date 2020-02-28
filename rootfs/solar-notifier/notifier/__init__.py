from flask import Flask
from notifier.utils import get_instance_folder_path
from notifier.config import configure_app


def _force_https(app):
    def wrapper(environ, start_response):
        environ['wsgi.url_scheme'] = 'https'
        return app(environ, start_response)
    return wrapper


app = Flask(__name__,
            instance_path=get_instance_folder_path(),
            instance_relative_config=True,
            static_folder='static')
configure_app(app)

with app.app_context():
    from notifier.api.controllers import api_bp
    from notifier.admin.controllers import admin, login_manager
    from notifier.data.models import db

db.init_app(app)
login_manager.init_app(app)
admin.init_app(app)
app.register_blueprint(api_bp, url_prefix='/api')
app = _force_https(app)
