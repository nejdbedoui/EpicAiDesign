from mongoengine import Document, StringField, ReferenceField, DateTimeField

import ImageApp.models
import PoemApp.models
import SpeechApp.models
import UserApp.models
import VideoApp.models
from MusicApp.models import MusicArt


class Reel(Document):
    title = StringField(max_length=400)
    track = ReferenceField(MusicArt)
    video = ReferenceField(VideoApp.models.GeneratedVideo)
    image = ReferenceField(ImageApp.models.ImageArt)
    poem = ReferenceField(PoemApp.models.PoemArt)
    speech = ReferenceField(SpeechApp.models.Speech)
    user = ReferenceField(UserApp.models.User)
    created_at = DateTimeField()
