import base64
import os
from datetime import datetime
from io import BytesIO

from django.contrib import messages
from django.shortcuts import render, redirect
import requests
from django.http import HttpResponse
from django.conf import settings
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
        payload = {
            'prompts': [category, prompt]
        }
        if action == 'generate':
            generate(request, category, prompt, payload, default)
        elif action == 'save' and default:
            save(request, category, prompt, default)
    return render(request, 'addmusic.html', {'base64_audio': default,'category_default': category, 'category': "Happy – Pharrell"})


def generate(request, category, prompt, payload, default):
    response = requests.post(MUSIC_Ai_API_URL, json=payload)
    if response.status_code == 200:
        audio_content = response.content
        encoded_string = base64.b64encode(audio_content).decode('utf-8')
        base64_audio = f"data:audio/mp3;base64,{encoded_string}"
        default = base64_audio
        return render(request, 'addmusic.html', {
            'base64_audio': base64_audio,
            'category_default': category,
            'prompt_default': prompt,
            'category': f"{category} - {prompt}"
        })
    else:
        messages.error(request,
                       f"Error: {response.status_code} - {response.json().get('error', 'Unknown error')}")
        return render(request, 'addmusic.html',
                      {'base64_audio': default, 'category_default': category, 'prompt_default': prompt,
                       'category': f"{category} - {prompt}"})


def save(request, category, prompt, default):
    audio_data = default.split(',')[1]
    audio_bytes = base64.b64decode(audio_data)
    audio_file = BytesIO(audio_bytes)
    music_art = MusicArt(
        title=f"{category} - {prompt}",
        category=category,
        audio=audio_file,
        duration=0.0,
        created_at=datetime.now()

    )
    music_art.save()
    messages.success(request, "Your music has been saved successfully!")
    return render(request, 'addmusic.html', {
        'base64_audio': default,
        'category_default': category,
        'prompt_default': prompt
    })