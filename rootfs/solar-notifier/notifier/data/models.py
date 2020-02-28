from flask_mongoengine import MongoEngine
from flask import current_app


db = MongoEngine()


class Channels(db.Document):
    name = db.StringField(max_length=40)
    token = db.StringField(max_length=40)

    def __unicode__(self):
        return self.name


class User(db.Document):
    name = db.StringField(max_length=40)
    token = db.StringField(max_length=40)
    telegramNick = db.StringField(max_length=40)
    chatId = db.IntField()
    channels = db.ListField(db.ReferenceField(Channels, reverse_delete_rule=4),
                            default=[])

    def __unicode__(self):
        return self.name


class Administrator(object):
    id = 1
    username = current_app.config.get('ADMIN_NAME')
    password = current_app.config.get('ADMIN_PASSWORD')

    # Flask-Login integration
    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id

    # Required for administrative interface
    def __unicode__(self):
        return self.username