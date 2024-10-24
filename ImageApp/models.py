from mongoengine import Document, StringField, FileField, DateTimeField


class ImageArt(Document):
    title = StringField(max_length=200)
    image = FileField()
    category = StringField(max_length=100)
    created_at = DateTimeField()
