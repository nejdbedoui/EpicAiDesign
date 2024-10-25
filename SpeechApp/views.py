import base64
import os

from django.conf import settings
from django.shortcuts import render


# Create your views here.
def Add_speech(request):
    # Path to the MP3 file (adjust this based on your setup)
    audio_path =  os.path.join(settings.BASE_DIR, 'static', 'assets', 'music', 'speech_ai.mp3')
    # Read and encode the file in Base64
    with open(audio_path, "rb") as audio_file:
        encoded_string = base64.b64encode(audio_file.read()).decode('utf-8')

    # Construct a data URL for the MP3 file
    base64_audio = f"data:audio/mp3;base64,{encoded_string}"

    return render(request, 'addSpeech.html', {'base64_audio': base64_audio})
