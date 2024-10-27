from datetime import datetime

from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect

import ImageApp.models
import MusicApp.models
import PoemApp.models
import ReelApp.models
import SpeechApp.models
import VideoApp.models
from UserApp.models import User


# Create your views here.
def add_reel(request):
    user_email = request.session.get('user_email')
    user = User.objects(email=user_email).first()
    music = MusicApp.models.MusicArt.objects.filter(user=user.id).only('id', 'title')
    images = ImageApp.models.ImageArt.objects.filter(user=user.id).only('id', 'title')
    videos = VideoApp.models.GeneratedVideo.objects.filter(user=user.id).only('id', 'name')
    poem = PoemApp.models.PoemArt.objects.filter(user=user.id).only('id', 'title')
    speech = SpeechApp.models.Speech.objects.filter(user=user.id).only('id', 'name')
    if request.method == "POST":
        title = request.POST.get("title")
        music_id = request.POST.get("selected_music")
        image_id = request.POST.get("selected_image")
        video_id = request.POST.get("selected_video")
        poem_id = request.POST.get("selected_poem")
        speech_id = request.POST.get("selected_speech")
        selected_track = MusicApp.models.MusicArt.objects(id=music_id).first() if music_id else None
        selected_image = ImageApp.models.ImageArt.objects(id=image_id).first() if image_id else None
        selected_video = VideoApp.models.GeneratedVideo.objects(id=video_id).first() if video_id else None
        selected_poem = PoemApp.models.PoemArt.objects(id=poem_id).first() if poem_id else None
        selected_speech = SpeechApp.models.Speech.objects(id=speech_id).first() if speech_id else None
        if selected_track is None and selected_image is None and selected_video is None and selected_poem is None and selected_speech is None:
            messages.error(request, 'Reel is Empty Required at least one element selected!')
        else:
            reel = ReelApp.models.Reel(
                title=title,
                track=selected_track,
                video=selected_video,
                image=selected_image,
                poem=selected_poem,
                speech=selected_speech,
                user=user,
                created_at=datetime.now(),
            )
            reel.save()
            return redirect('Gallery')
    return render(request, 'add_reel.html',
                  {'music': music, 'images': images, 'videos': videos, 'poem': poem, 'speech': speech})


def reels_show(request):
    user_id = request.session.get('user_id')
    reels = ReelApp.models.Reel.objects.filter(user=user_id).order_by('created_at')
    return render(request, 'Reels_Show.html', {'reels': reels})

