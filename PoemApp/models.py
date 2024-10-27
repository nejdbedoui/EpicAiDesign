from mongoengine import Document, StringField, DateTimeField, FloatField, BooleanField, ReferenceField
import UserApp.models



class PoemArt(Document):
    title = StringField(max_length=200)
    category = StringField(max_length=100)
    text = StringField()
    public = BooleanField()
    rating = FloatField()
    created_at = DateTimeField()
    user = ReferenceField(UserApp.models.User)
    license = ReferenceField('License')  # Assurez-vous que License est défini et importé

class License(Document):
    name = StringField(max_length=100, required=True)
    description = StringField()
    created_at = DateTimeField()
    user = ReferenceField(UserApp.models.User)
    poem = ReferenceField(PoemArt)  # Ajoutez cette ligne pour établir la relation avec PoemArt
