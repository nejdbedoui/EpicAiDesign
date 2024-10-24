from mongoengine import Document, StringField, DateTimeField, FloatField


class PoemArt(Document):
    title = StringField(max_length=200)
    category = StringField(max_length=100)
    text = StringField()
    created_at = DateTimeField()
