from mongoengine import Document, StringField, FileField, DateTimeField, FloatField, BooleanField


class MusicArt(Document):
    title = StringField(max_length=400)
    category = StringField(max_length=100)
    audio = FileField()
    duration = FloatField()
    public = BooleanField()
    created_at = DateTimeField()
