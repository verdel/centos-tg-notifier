from flask_admin.contrib.mongoengine import ModelView
from wtforms.validators import required, regexp
from flask_admin.form import rules
from flask_admin import expose, helpers, AdminIndexView
from flask import redirect, url_for, request
import flask_login as login
from notifier.admin.forms import LoginForm


class UserView(ModelView):

    form_create_rules = ['name', rules.Field('token', 'rule_token.render_field'), 'telegramNick', 'chatId', 'channels']
    form_edit_rules = form_create_rules
    create_template = 'admin/rule_create.html'
    edit_template = 'admin/rule_edit.html'

    form_args = {
        'name': {
            'label': 'User',
            'validators': [required()]
        },

        'token': {
            'label': 'Token',
            'validators': [required(), regexp('^(?=.*\d)(?=.*[a-z])[0-9a-z]{32}$', message='Token must be 32 characters long and must contain at least 1 number and 1 letter')]
        },

        'telegramNick': {
            'label': 'Telegram Nick',
        },

        'chatId': {
            'label': 'Telegram ChatId',
        },

        'channels': {
            'label': 'Channels',
            'allow_blank': True,
            'blank_text': 'Select to clear field'
        }
    }

    form_widget_args = {
        'telegramNick': {
            'readonly': True
        },

        'chatId': {
            'readonly': True
        },

        'channels': {
            'placeholder': 'Please select channels'
        }
    }
    column_searchable_list = ['name', 'telegramNick']
    column_filters = ['name', 'telegramNick']
    column_labels = dict(name='User', token='Token', telegramNick='Telegram Nickname', chatId='Telegram Chat Id')

    def is_accessible(self):
        return login.current_user.is_authenticated


class ChannelsView(ModelView):

    form_create_rules = ['name', rules.Field('token','rule_token.render_field')]
    form_edit_rules = form_create_rules
    create_template = 'admin/rule_create.html'
    edit_template = 'admin/rule_edit.html'
    form_args = {
        'name': {
            'label': 'User',
            'validators': [required()]
        },

        'token': {
            'label': 'Token',
            'validators': [required(), regexp('^(?=.*\d)(?=.*[a-z])[0-9a-z]{32}$', message='Token must be 32 characters long and must contain at least 1 number and 1 letter')]
        }
    }
    column_labels = dict(name='Channel', token='Token')

    def is_accessible(self):
        return login.current_user.is_authenticated


class MyAdminIndexView(AdminIndexView):
    @expose('/')
    def index(self):
        if not login.current_user.is_authenticated:
            return redirect(url_for('.login_view'))
        return super(MyAdminIndexView, self).index()

    @expose('/login/', methods=('GET', 'POST'))
    def login_view(self):
        # handle user login
        form = LoginForm(request.form)
        if helpers.validate_form_on_submit(form):
            user = form.get_user()
            login.login_user(user)

        if login.current_user.is_authenticated:
            return redirect(url_for('.index'))
        self._template_args['form'] = form
        return super(MyAdminIndexView, self).index()

    @expose('/logout/')
    def logout_view(self):
        login.logout_user()
        return redirect(url_for('.index'))
