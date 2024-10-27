from datetime import datetime
from django.shortcuts import render, redirect,get_object_or_404
from django.contrib import messages
from EpicAiDesign.External_url import poeme_Ai_API_URL
from PoemApp.models import PoemArt,License
import requests
from mongoengine.errors import DoesNotExist
from django.shortcuts import redirect
from bson import ObjectId

from .models import PoemArt, License
import UserApp.models



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
        # Ajouter un message de succès
        messages.success(request, 'Poème mis à jour avec succès !')
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

def add_license(request, id):
    try:
        poem = PoemArt.objects.get(id=id)
    except PoemArt.DoesNotExist:
        return render(request, '404.html')

    if request.method == 'POST':
        license_name = request.POST.get('license_name')
        license_description = request.POST.get('license_description')

        if not license_name:
            messages.error(request, "Le nom de la licence est requis.")
            return render(request, 'add_license.html', {'poem': poem})
        user = UserApp.models.User.objects.get(email=request.session['user_email'])

        new_license = License(
            name=license_name,
            description=license_description,
            created_at=datetime.now(),
            poem=poem,
            user=user
        )

        try:
            new_license.save()
        except Exception as e:
            messages.error(request, f"Erreur lors de l'enregistrement de la licence : {str(e)}")
            return render(request, 'add_license.html', {'poem': poem})

        poem.license = new_license
        poem.save()

        messages.success(request, 'Licence ajoutée avec succès.')
        return redirect('Gallery')

    return render(request, 'add_license.html', {'poem': poem})



def license_list(request):

    # Récupérer toutes les licences sans select_related
    licenses = License.objects.all()  
    return render(request, 'licenses.html', {'licenses': licenses})


def license_details(request, id):
    try:
        license_id = ObjectId(id)
        license_item = License.objects.get(id=license_id)
        print(f"Retrieved license: {license_item}")  # Debugging line
        return render(request, 'license_details.html', {'license_item': license_item})

    except DoesNotExist:
        print("License does not exist.")  # Debugging line
        return render(request, '404.html', status=404)

def delete_license(request, id):
    if request.method == 'POST':
        try:
            # Utilisez get_object_or_404 pour rechercher la licence
            license_item = License.objects.get(id=id)
            license_item.delete()
            messages.success(request, "La licence a été supprimée avec succès.")  
        except License.DoesNotExist:
            messages.error(request, "La licence n'existe pas.") 

        return redirect('Gallery')  

    return redirect('Gallery') 