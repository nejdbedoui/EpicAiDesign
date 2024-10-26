import base64
import os
from datetime import datetime
from io import BytesIO

from django.contrib import messages
from django.shortcuts import render
import requests
from django.conf import settings

import UserApp.models
from EpicAiDesign.External_url import *
from MusicApp.models import MusicArt


def default_audio():
    audio_path = os.path.join(settings.BASE_DIR, 'static', 'assets', 'music', 'djappa3.mp3')
    with open(audio_path, "rb") as audio_file:
        encoded_string = base64.b64encode(audio_file.read()).decode('utf-8')
    base64_audio = f"data:audio/mp3;base64,{encoded_string}"
    return base64_audio


def Generate_music(request):
    default = default_audio()
    category = "Classical music"
    if request.method == 'POST':
        category = request.POST.get('category')
        prompt = request.POST.get('prompt')
        action = request.POST.get('action')
        title = request.POST.get('title')
        payload = {
            'prompts': [category, prompt]
        }
        if action == 'generate':
            title = f"{category} - {prompt}"
            return generate(request, title, category, prompt, payload, default)
        elif action == 'save' and default:
            audio = request.POST.get('audio')
            return save(request, title, category, prompt, audio)
    return render(request, 'addmusic.html',
                  {'base64_audio': default, 'title': "Happy – Pharrell", 'category': category})


def generate(request, title, category, prompt, payload, default):
    response = requests.post(MUSIC_Ai_API_URL, json=payload)
    if response.status_code == 200:
        audio_content = response.content
        encoded_string = base64.b64encode(audio_content).decode('utf-8')
        base64_audio = f"data:audio/mp3;base64,{encoded_string}"
        return render(request, 'addmusic.html', {
            'base64_audio': base64_audio,
            'prompt_default': prompt,
            'category': category,
            'title': title
        })
    else:
        messages.error(request,
                       f"Error: {response.status_code} - {response.json().get('error', 'Unknown error')}")
        return render(request, 'addmusic.html',
                      {'base64_audio': default, 'prompt_default': prompt,
                       'category': f"{category}"})


def save(request, title, category, prompt, default):
    audio_data = default.split(',')[1]
    audio_bytes = base64.b64decode(audio_data)
    audio_file = BytesIO(audio_bytes)
    user = UserApp.models.User.objects.get(email=request.session['user_email'])
    music_art = MusicArt(
        title=title,
        category=category,
        audio=audio_file,
        duration=0.0,
        created_at=datetime.now(),
        user=user
    )
    music_art.save()
    messages.success(request, "Your music has been saved successfully!")
    return render(request, 'addmusic.html', {
        'base64_audio': default,
        'category': category,
        'prompt_default': prompt,
        'title': title
    })


def Details_music(request, id):
    music = MusicArt.objects(id=id).first()
    encoded_string = base64.b64encode(music.audio.read()).decode('utf-8')
    base64_audio = f"data:audio/mp3;base64,{encoded_string}"
    print(music.audio.read())
    return render(request, 'detailsmusic.html', {'base64_audio': base64_audio, 'music': music})
