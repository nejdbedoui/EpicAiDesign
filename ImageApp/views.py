import base64
import os
from datetime import datetime
from io import BytesIO

from django.contrib import messages
from django.shortcuts import render
import requests
from django.conf import settings
from EpicAiDesign.External_url import *
from ImageApp.models import ImageArt


def Generate_image(request):
    category = "Draw Image"
    if request.method == 'POST':
        category = request.POST.get('category')
        prompt = request.POST.get('prompt', '').strip() or "draw a cat"
        action = request.POST.get('action')
        title = request.POST.get('title')

        payload = {
            'prompt': f"{category} - {prompt}"  # Combine category et prompt en une seule chaîne
        }

        if action == 'generate':
            title = f"{category} - {prompt}"
            return generate(request, title, category, prompt, payload)
        elif action == 'save':
            image_data = request.POST.get('image_data')
            return save(request, title, category, prompt, image_data)

    return render(request, 'addimage.html', {
        'title': "Artistic Vision",
        'category': category,
        'prompt_default': "Draw Art design for A Cat"  # Pour affichage initial
    })




def generate(request, title, category, prompt, payload):
    print("Payload envoyé à l'API:", payload)  # Débogage
    response = requests.post(IMAGE_Ai_API_URL, json=payload)
    if response.status_code == 200:
        image_content = response.content
        encoded_string = base64.b64encode(image_content).decode('utf-8')
        base64_image = f"data:image/png;base64,{encoded_string}"
        return render(request, 'addimage.html', {
            'base64_image': base64_image,
            'prompt_default': prompt,
            'category': category,
            'title': title
        })
    else:
        messages.error(request,
                       f"Error: {response.status_code} - {response.json().get('error', 'Unknown error')}")
        return render(request, 'addimage.html', {
            'prompt_default': prompt,
            'category': category
        })


def save(request, title, category, prompt, image_data):
    image_data = image_data.split(',')[1]  # Enlever la partie 'data:image/png;base64,'
    image_bytes = base64.b64decode(image_data)
    image_file = BytesIO(image_bytes)
    image_art = ImageArt(
        title=title,
        category=category,
        image=image_file,
        created_at=datetime.now()
    )
    image_art.save()
    messages.success(request, "Your image has been saved successfully!")
    return render(request, 'addimage.html', {
        'category': category,
        'prompt_default': prompt,
        'title': title
    })