from mongoengine import Document, StringField, DateTimeField, FloatField, ListField, \
    ImageField, ReferenceField, EmbeddedDocument, EmbeddedDocumentField

from MusicApp.models import MusicArt
import UserApp.models
from django.core.exceptions import ObjectDoesNotExist


class UserRating(EmbeddedDocument):
    user = ReferenceField(UserApp.models.User, required=True)
    rating = FloatField(required=True, min_value=1, max_value=5)


class MusicAlbum(Document):
    title = StringField(max_length=400)
    cover = ImageField()
    rating = FloatField()
    description = StringField(max_length=500)
    created_at = DateTimeField()
    tracks = ListField(ReferenceField(MusicArt))
    user = ReferenceField(UserApp.models.User)
    user_rated = ListField(EmbeddedDocumentField(UserRating))
