from django.shortcuts import render, redirect
from django.http import HttpResponse, FileResponse
from .forms import SpeechForm, UpdateSpeechForm
from .models import Speech
from UserApp.decorator import custom_login_required
import requests
import os
from django.conf import settings
import uuid
from base64 import b64encode


@custom_login_required
def add_speech(request):
    user_id = request.session.get('user_id')
    if request.method == 'POST':
        form = SpeechForm(request.POST, request.FILES)
        if form.is_valid():
            data = form.cleaned_data

            response = requests.post(
                'http://localhost:5000/synthesize',
                json={'text': data['text']}
            )
            if response.status_code == 200:
                speech_file_name = f"{data['name']}_{uuid.uuid4()}.mp3"
                speech_file_path = os.path.join(settings.MEDIA_ROOT, speech_file_name)
                with open(speech_file_path, 'wb') as f:
                    f.write(response.content)

                sppech = Speech(
                    name=data['name'],
                    text=data['text'],
                    display=data['display'],
                    speech_file=speech_file_path,
                    user=user_id
                )
                sppech.save()

                return redirect('list_speechs')
            else:
                form.add_error(None, 'Error generating speech from service.')
        else:
            form.add_error(None, 'Form data is not valid.')
    else:
        form = SpeechForm()
    return render(request, 'add_speech.html', {'form': form})


@custom_login_required
def update_speech(request, speech_id):
    speech = Speech.objects.get(id=speech_id)

    if request.method == 'POST':
        form = UpdateSpeechForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data

            # Mettre à jour les champs speech
            speech.name = data['name']
            speech.display = data['display']
            speech.save()

            return redirect('list_speechs')
    else:
        # Pré-remplir le formulaire avec les informations de la speech
        form = UpdateSpeechForm(initial={
            'name': speech.name,
            'display': speech.display
        })
    return render(request, 'update_speech.html', {'form': form, 'speech': speech})


@custom_login_required
def speech_list(request):
    user_id = request.session.get('user_id')

    speechs = Speech.objects.filter(display=True)

    return render(request, 'speech_list.html', {'speechs': speechs})


@custom_login_required
def speech_listUser(request):
    user_id = request.session.get('user_id')
    speechs = Speech.objects.filter(user=user_id)
    return render(request, 'speech_list.html', {'speechs': speechs})


@custom_login_required
def delete_speech(request, speech_id):
    speech = Speech.objects.get(id=speech_id)

    if speech.speech_file and os.path.isfile(speech.speech_file):
        os.remove(speech.speech_file)

    speech.delete()
    return redirect('list_speechs')


@custom_login_required
def get_speech(request, speech_id):
    user_id = request.session.get('user_id')

    speech = Speech.objects.get(id=speech_id)
    blogs = speech.blogs

    for blog in blogs:
        if blog.user.image:
            image = blog.user.image.read()
            encoded_image = b64encode(image).decode('utf-8')
            blog.user.image_url = f"data:image/jpeg;base64,{encoded_image}"
        else:
            blog.user.image_url = None

    return render(request, 'speech_detail.html', {'speech': speech, 'blogs': blogs, 'user_id': user_id})

@custom_login_required
def serve_audio(request, speech_id):
    try:
        # Assumer que `Speech` est votre modèle et il contient un champ `speech_file`
        speech = Speech.objects.get(id=speech_id)
        # Chemin vers le fichier audio
        file_path = speech.speech_file
        # Créer une réponse qui sert le fichier
        response = FileResponse(open(file_path, 'rb'), content_type='audio/mp3')
        response['Content-Disposition'] = 'inline; filename="{}"'.format(speech.name)
        return response
    except Speech.DoesNotExist:
        return HttpResponse("Audio not found", status=404)