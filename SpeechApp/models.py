from mongoengine import Document, StringField, FileField, DateTimeField, FloatField


class Speech(Document):
    title = StringField(max_length=200)
    speech = FileField()
    category = StringField(max_length=100)
    created_at = DateTimeField()
