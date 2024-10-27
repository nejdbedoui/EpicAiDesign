from mongoengine import Document, StringField, DateTimeField, ReferenceField
from datetime import datetime
from UserApp.models import User

class Blog(Document):
    text = StringField(required=True, verbose_name="Commentaire")
    created_at = DateTimeField(default=datetime.now, verbose_name="Date de création")
    user = ReferenceField(User, required=True, verbose_name="Utilisateur")
    speech = ReferenceField('SpeechApp.models.Speech', required=True, verbose_name="Speech")