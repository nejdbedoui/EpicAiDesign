from mongoengine import Document, StringField, FileField, DateTimeField, BooleanField


class ImageArt(Document):
    title = StringField(max_length=200)
    image = FileField()
    category = StringField(max_length=100)
    public = BooleanField()
    created_at = DateTimeField()
