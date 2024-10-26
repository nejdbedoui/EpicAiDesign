import base64
import os
from datetime import datetime
from io import BytesIO
from django.http import HttpResponseRedirect

from django.contrib import messages
from django.shortcuts import render
import requests
from django.conf import settings
from EpicAiDesign.External_url import *
from ImageApp.models import ImageArt


def Generate_image(request):
    category = "Draw Image"
    images = ImageArt.objects.all()
    if request.method == 'POST':
        category = request.POST.get('category')
        prompt = request.POST.get('prompt', '').strip() or "a sleek Mercedes-Benz speeding on a winding road, with blurred scenery in the background"
        action = request.POST.get('action')
        title = request.POST.get('title')

        payload = {
            'prompt': f"{category} - {prompt}"  # Combine category et prompt en une seule chaîne
        }

        if action == 'generate':
            title = f"{category} - {prompt}"
            return generate(request, title, category, prompt, payload)
        elif action == 'save':
            base64_image = request.POST.get('base64_image')
            return save(request, title, category, prompt, base64_image, images)  # Passer les images à la méthode save

    return render(request, 'addimage.html', {
        'title': "Real Image",
        'category': category,
        'prompt_default': "a sleek Mercedes-Benz speeding on a winding road, with blurred scenery in the background",
        'images': images  # Passer toutes les images à la template
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
            'title': title,
            'images': ImageArt.objects.all()  # Récupérer toutes les images pour affichage
        })
    else:
        messages.error(request,
                       f"Error: {response.status_code} - {response.json().get('error', 'Unknown error')}")
        return render(request, 'addimage.html', {
            'prompt_default': prompt,
            'category': category,
            'images': ImageArt.objects.all()  # Récupérer toutes les images pour affichage
        })


def save(request, title, category, prompt, base64_image, images):
    if base64_image is None:
        messages.error(request, "No image data found. Please generate an image first.")
        return render(request, 'addimage.html', {
            'category': category,
            'prompt_default': prompt,
            'title': title,
            'images': images
        })

    image_data = base64_image.split(',')[1]
    image_bytes = base64.b64decode(image_data)
    image_file = BytesIO(image_bytes)

    # Enregistrer l'image dans la base de données
    image_art = ImageArt(
        title=title,
        category=category,
        created_at=datetime.now()
    )
    image_art.image.put(image_file, content_type="image/png")
    image_art.save()

    messages.success(request, "Your image has been saved successfully!")
    images = ImageArt.objects.all()  # Récupérer toutes les images après enregistrement

    return render(request, 'addimage.html', {
        'category': category,
        'prompt_default': prompt,
        'title': title,
        'base64_image':base64_image,
        'images': images  # Passer toutes les images à la template
    })
