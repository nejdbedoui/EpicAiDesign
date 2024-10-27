<<<<<<< HEAD
from mongoengine import Document, StringField, DateTimeField, FloatField, BooleanField


=======
from mongoengine import Document, StringField, DateTimeField, FloatField, BooleanField, ReferenceField
import UserApp.models

>>>>>>> 31048a1ab8292946577aeb18d50c15ac8b018416
class PoemArt(Document):
    title = StringField(max_length=200)
    category = StringField(max_length=100)
    text = StringField()
    public = BooleanField()
    rating = FloatField()
    created_at = DateTimeField()
    user = ReferenceField(UserApp.models.User)
