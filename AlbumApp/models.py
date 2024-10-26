from mongoengine import Document, StringField, DateTimeField, FloatField, ListField, \
    ImageField, ReferenceField

from MusicApp.models import MusicArt
import UserApp.models
from django.core.exceptions import ObjectDoesNotExist


class MusicAlbum(Document):
    title = StringField(max_length=400)
    cover = ImageField()
    rating = FloatField()
    created_at = DateTimeField()
    tracks = ListField(ReferenceField(MusicArt))
    user = ReferenceField(UserApp.models.User)