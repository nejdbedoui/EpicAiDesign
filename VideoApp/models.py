from mongoengine import Document, StringField, DateTimeField, FloatField
from embed_video.fields import EmbedVideoField


class MusicArt(Document):
    title = StringField(max_length=200)
    video = EmbedVideoField()
    duration = FloatField()
    created_at = DateTimeField()
