from mongoengine import Document, StringField, DateTimeField, FloatField, ListField, ImageField, ReferenceField
from ImageApp.models import ImageArt
import UserApp.models

class ImageGallery(Document):
    title = StringField(max_length=400)
    cover = ImageField()
    rating = FloatField()
    created_at = DateTimeField()
    images = ListField(ReferenceField(ImageArt))
    user = ReferenceField(UserApp.models.User)
