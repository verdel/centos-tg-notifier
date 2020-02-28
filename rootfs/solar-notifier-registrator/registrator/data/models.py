from mongoengine import *


class Channels(Document):
    name = StringField(max_length=40)
    token = StringField(max_length=40)

    def __unicode__(self):
        return self.name


class User(Document):
    name = StringField(max_length=40)
    token = StringField(max_length=40)
    telegramNick = StringField(max_length=40)
    chatId = IntField()
    channels = ListField(ReferenceField(Channels, reverse_delete_rule=4),
                         default=[])

    def __unicode__(self):
        return self.name
