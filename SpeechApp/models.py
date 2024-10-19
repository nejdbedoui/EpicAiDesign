from mongoengine import Document, StringField, FileField, DateTimeField, FloatField


class Speech(Document):
    title = StringField(max_length=200)
    animation = FileField()
    created_at = DateTimeField()
