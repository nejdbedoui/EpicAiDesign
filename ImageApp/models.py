from mongoengine import Document, StringField, FileField, DateTimeField, BooleanField, FloatField


class ImageArt(Document):
    title = StringField(max_length=200)
    image = FileField()
    category = StringField(max_length=100)
    public = BooleanField()
    rating = FloatField()
    created_at = DateTimeField()
