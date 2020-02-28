import flask_login as login
from flask_admin import Admin
from notifier.data.models import *
from notifier.admin.views import *


login_manager = login.LoginManager()


@login_manager.user_loader
def load_user(user_id):
    return Administrator()

admin = Admin(name='Notifier', index_view=MyAdminIndexView(url='/'), template_mode='bootstrap3', base_template='my_master.html')
admin.add_view(UserView(User))
admin.add_view(ChannelsView(Channels))
