from mongoengine import Document, StringField, DateTimeField, FloatField, BooleanField


class PoemArt(Document):
    title = StringField(max_length=200)
    category = StringField(max_length=100)
    text = StringField()
    public = BooleanField()
    created_at = DateTimeField()
