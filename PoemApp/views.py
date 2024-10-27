from datetime import datetime
from django.shortcuts import render, redirect
from django.contrib import messages

import UserApp.models
from EpicAiDesign.External_url import poeme_Ai_API_URL
from PoemApp.models import PoemArt
import requests
from mongoengine.errors import DoesNotExist
from django.shortcuts import redirect, get_object_or_404
from .models import PoemArt  # Assurez-vous que votre modèle est bien importé


def Add_poem(request):
    category = "musique"
    if request.method == 'POST':
        category = request.POST.get('category')
        prompt = request.POST.get('prompt')
        action = request.POST.get('action')
        title = request.POST.get('title')
        text = request.POST.get('text')
        if action == 'generate':
            return generate(request, title, category, prompt)
        elif action == 'save':
            print(category)
            return save(request, title, category, prompt, text)
    return render(request, 'addPoem.html',
                  {'title': "", 'category': category})


def generate(request, title, category, prompt):
    # Prepare the JSON payload
    payload = {
        "prompt": prompt,
        "category": category,
        "max_length": 200  # Adjust the length as needed
    }
    
    try:
        # Send a POST request to the poem AI API
        response = requests.post(poeme_Ai_API_URL, json=payload)
        response.raise_for_status()  # Raise an exception for HTTP error responses

        # Parse the JSON response
        response_data = response.json()
        text = response_data.get("poem", "")  # Get the poem from the response JSON

    except requests.exceptions.RequestException as e:
        # Handle request errors (network issues, server errors, etc.)
        messages.error(request, f"Error generating poem: {str(e)}")
        text = ""

    return render(request, 'addPoem.html',
                  {'title': title, 'category': category, 'prompt': prompt, 'text': text})
def save(request, title, category, prompt, text):
    user = UserApp.models.User.objects.get(email=request.session['user_email'])
    poem = PoemArt(
        title=title,
        category=category,
        text=text,
        created_at=datetime.now(),
        user=user
    )
    poem.save()
    messages.success(request, "Your music has been saved successfully!")
    return render(request, 'addPoem.html', {'title': title, 'category': category, 'prompt': prompt, 'text': text})

def Details_poeme(request, id):
    poeme = PoemArt.objects(id=id).first()
    return render(request, 'detailspoeme.html', { 'poeme': poeme})

def update_poem(request, id):
    try:
        # Récupérer le poème avec l'ID donné
        poem = PoemArt.objects.get(id=id)
    except DoesNotExist:
        return render(request, '404.html')  # Gérez comme vous le souhaitez

    if request.method == 'POST':
        title = request.POST.get('title')
        text = request.POST.get('text')
        # Mettre à jour les champs
        poem.title = title
        poem.text = text
        poem.save()
        return redirect('Gallery')  # Cela semble correct

    return render(request, 'update_poem.html', {'poem': poem})

def delete_poem(request, id):
    if request.method == 'POST':
        try:
            
            poem = PoemArt.objects.get(id=id)
            poem.delete()  
            messages.success(request, "Le poème a été supprimé avec succès.")
        except DoesNotExist:
            messages.error(request, "Le poème n'existe pas.")  
        return redirect('Gallery')  

    return redirect('Gallery') 

