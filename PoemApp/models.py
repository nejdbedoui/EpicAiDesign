from mongoengine import Document, StringField, DateTimeField, FloatField


class PoemArt(Document):
    title = StringField(max_length=200)
    type = StringField()
    text = StringField()
    created_at = DateTimeField()
