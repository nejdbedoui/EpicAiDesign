from mongoengine import Document, StringField, BooleanField, DateTimeField, ListField, ReferenceField
from datetime import datetime
from UserApp.models import User
from TagsVideoApp.models import Tag

class GeneratedVideo(Document):
    name = StringField(max_length=255, required=True, verbose_name="Nom de la vidéo")
    prompt = StringField(required=True, verbose_name="Description utilisée pour générer la vidéo")
    display = BooleanField(default=True, verbose_name="Afficher la vidéo")
    created_at = DateTimeField(default=datetime.now, verbose_name="Date de création")
    user = ReferenceField(User, required=True, verbose_name="Utilisateur")
    video_file = StringField(required=True, verbose_name="Chemin du fichier vidéo")
    tags = ListField(ReferenceField(Tag), verbose_name="Tags associés")

