from mongoengine import Document, StringField, FileField, DateTimeField, FloatField


class MusicArt(Document):
    title = StringField(max_length=200)
    video = FileField()
    duration = FloatField()
    created_at = DateTimeField()
