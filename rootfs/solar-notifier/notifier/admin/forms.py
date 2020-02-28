from wtforms import form, fields, validators
from notifier.data.models import Administrator


class LoginForm(form.Form):
    login = fields.TextField(validators=[validators.required()])
    password = fields.PasswordField(validators=[validators.required()])

    def validate_login(self, field):
        user = self.get_user()
        if user.username != self.login.data:
            raise validators.ValidationError('Invalid user')

    def validate_password(self, field):
        user = self.get_user()
        if user.password != self.password.data:
            raise validators.ValidationError('Invalid password')

    def get_user(self):
        return Administrator()
