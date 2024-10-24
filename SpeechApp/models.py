from mongoengine import Document, StringField, FileField, DateTimeField, FloatField, BooleanField


class Speech(Document):
    title = StringField(max_length=200)
    speech = FileField()
    category = StringField(max_length=100)
    public = BooleanField()
    created_at = DateTimeField()
