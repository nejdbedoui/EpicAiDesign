from datetime import datetime

from django.shortcuts import render
from django.contrib import messages
from PoemApp.models import PoemArt
import requests
from EpicAiDesign.External_url import poeme_Ai_API_URL




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
    payload = {
        "prompt": prompt,
        "category": category,
        "max_length": 200  # You can change this value as needed
    }
    response = requests.post(poeme_Ai_API_URL, json=payload)
    
    data = response.json()
    text = data.get('poem', 'No poem generated.')


    return render(request, 'addPoem.html',
                  {'title': title, 'category': category, 'prompt': prompt, 'text': text})



def save(request, title, category, prompt, text):
    poem = PoemArt(
        title=title,
        category=category,
        text=text,
        created_at=datetime.now()
    )
    poem.save()
    messages.success(request, "Your music has been saved successfully!")
    return render(request, 'addPoem.html', {'title': title, 'category': category, 'prompt': prompt, 'text': text})

