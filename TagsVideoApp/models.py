from mongoengine import Document, StringField, ListField, ReferenceField
from UserApp.models import User

class Tag(Document):
    name = StringField(required=True, unique=True, verbose_name="Nom du tag")
    videos = ListField(ReferenceField('VideoApp.models.GeneratedVideo'), verbose_name="Vidéos associées")
    user = ReferenceField(User, required=True, verbose_name="Utilisateur")

    def __str__(self):
        return self.name