<<<<<<< HEAD
from mongoengine import Document, StringField, FileField, DateTimeField, BooleanField, FloatField
=======
from mongoengine import Document, StringField, ImageField, DateTimeField, BooleanField, FloatField
>>>>>>> 31048a1ab8292946577aeb18d50c15ac8b018416


class ImageArt(Document):
    title = StringField(max_length=200)
<<<<<<< HEAD
    image = FileField()
=======
    image = ImageField()
>>>>>>> 31048a1ab8292946577aeb18d50c15ac8b018416
    category = StringField(max_length=100)
    public = BooleanField()
    rating = FloatField()
    created_at = DateTimeField()

    def __str__(self):
        return self.title