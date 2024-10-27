from mongoengine import Document, StringField, ReferenceField, DateTimeField, BooleanField
from datetime import datetime
from UserApp.models import User

class Speech(Document):
    name = StringField(max_length=255, required=True, verbose_name="Nom de la sppech")
    text = StringField(required=True, verbose_name="Description utilisée pour générer le speech")
    display = BooleanField(default=True, verbose_name="Afficher le speech")
    created_at = DateTimeField(default=datetime.now, verbose_name="Date de création")
    user = ReferenceField(User, required=True, verbose_name="Utilisateur")
    speech_file = StringField(required=True, verbose_name="Chemin du fichier speech")

