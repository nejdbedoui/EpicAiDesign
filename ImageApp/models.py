from mongoengine import Document, StringField, FileField, DateTimeField


class ImageArt(Document):
    title = StringField(max_length=200)
    image = FileField()
    created_at = DateTimeField()
