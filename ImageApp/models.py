from mongoengine import Document, StringField, ImageField, DateTimeField, BooleanField, FloatField, ReferenceField

import UserApp.models


class ImageArt(Document):
    title = StringField(max_length=200)
    image = ImageField()
    category = StringField(max_length=100)
    public = BooleanField()
    rating = FloatField()
    created_at = DateTimeField()
    user = ReferenceField(UserApp.models.User)
    def __str__(self):
        return self.title