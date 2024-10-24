from mongoengine import Document, StringField, DateTimeField, FloatField
from embed_video.fields import EmbedVideoField


class VideoArt(Document):
    title = StringField(max_length=200)
    video = EmbedVideoField()
    duration = FloatField()
    category = StringField(max_length=100)
    rating = FloatField()
    created_at = DateTimeField()
