from mongoengine import Document, StringField, FileField, DateTimeField, FloatField


class MusicArt(Document):
    title = StringField(max_length=400)
    category = StringField(max_length=100)
    audio = FileField()
    duration= FloatField()
    created_at = DateTimeField()
