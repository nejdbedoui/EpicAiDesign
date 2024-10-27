from mongoengine import Document, StringField, FileField, DateTimeField, FloatField, BooleanField, ReferenceField

import UserApp.models


class MusicArt(Document):
    title = StringField(max_length=400)
    category = StringField(max_length=100)
    audio = FileField()
    duration = FloatField()
    public = BooleanField()
    rating = FloatField()
    created_at = DateTimeField()
    user = ReferenceField(UserApp.models.User)

