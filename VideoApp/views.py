from django.shortcuts import render, redirect
from django.http import HttpResponse, StreamingHttpResponse, FileResponse
from .forms import VideoForm, UpdateVideoForm, TagForm
from .models import GeneratedVideo
from TagsVideoApp.models import Tag
from UserApp.decorator import custom_login_required
import requests
import os
from django.conf import settings
import uuid
from bson import ObjectId

@custom_login_required
def add_video(request):
    user_id = request.session.get('user_id')
    tags = Tag.objects.all()
    if request.method == 'POST':
        form = VideoForm(request.POST, request.FILES)
        if form.is_valid():
            data = form.cleaned_data

            response = requests.post(
                'http://127.0.0.1:5001/generate_video',
                json={'prompt': data['prompt']}
            )
            if response.status_code == 200:
                video_file_name = f"{data['name']}_{uuid.uuid4()}.mp4"
                video_file_path = os.path.join(settings.MEDIA_ROOT, video_file_name)
                with open(video_file_path, 'wb') as f:
                    f.write(response.content)

                video = GeneratedVideo(
                    name=data['name'],
                    prompt=data['prompt'],
                    display=data['display'],
                    video_file=video_file_path,
                    user=user_id
                )
                video.save()

                # Associer les tags sélectionnés
                selected_tags = data['tags']  # Liste d'IDs des tags sélectionnés
                for tag_id in selected_tags:
                    tag = Tag.objects.get(id=ObjectId(tag_id))  # Utilisez ObjectId si MongoDB
                    if video not in tag.videos:
                        tag.videos.append(video)
                        tag.save()
                    if tag not in video.tags:
                        video.tags.append(tag)
                video.save()

                return redirect('list_videos')
            else:
                form.add_error(None, 'Error generating video from service.')
        else:
            form.add_error(None, 'Form data is not valid.')
    else:
        form = VideoForm()
    return render(request, 'add_video.html', {'form': form, 'tags': tags})

@custom_login_required
def update_video(request, video_id):
    video = GeneratedVideo.objects.get(id=video_id)
    tags = Tag.objects.all()  # Récupérer tous les tags pour les afficher dans le formulaire

    if request.method == 'POST':
        form = UpdateVideoForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data

            # Mettre à jour les champs vidéo
            video.name = data['name']
            video.display = data['display']
            video.save()

            # Gérer les tags
            selected_tags = data.get('tags', [])
            # Supprimer les tags non sélectionnés
            for tag in video.tags:
                if str(tag.id) not in selected_tags:
                    tag.videos.remove(video)
                    video.tags.remove(tag)
                    tag.save()

            # Ajouter les nouveaux tags sélectionnés
            for tag_id in selected_tags:
                tag = Tag.objects.get(id=tag_id)
                if video not in tag.videos:
                    tag.videos.append(video)
                    tag.save()
                if tag not in video.tags:
                    video.tags.append(tag)
            video.save()

            return redirect('list_videos')
    else:
        # Pré-remplir le formulaire avec les informations de la vidéo
        form = UpdateVideoForm(initial={
            'name': video.name,
            'display': video.display,
            'tags': [str(tag.id) for tag in video.tags]  # Pré-sélectionner les tags associés
        })

    return render(request, 'update_video.html', {'form': form, 'video': video, 'tags': tags})


@custom_login_required
def video_list(request):
    user_id = request.session.get('user_id')

    mytags = Tag.objects.filter(user=user_id)
    alltags = Tag.objects.all()

    selected_tag_id = request.GET.get('tag')

    if selected_tag_id:
        selected_tag = Tag.objects.get(id=selected_tag_id)
        videos = selected_tag.videos
    else:
        videos = GeneratedVideo.objects.filter(display=True)

    if request.method == 'POST':
        form = TagForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data

            tag = Tag(
                name=data['name'],
                user=user_id
            )
            tag.save()
            return redirect('list_videos')
    else:
        form = TagForm()

    return render(request, 'video_list.html', {'videos': videos, 'mytags': mytags, 'alltags': alltags, 'form': form, 'selected_tag': selected_tag_id})

@custom_login_required
def video_listUser(request):
    user_id = request.session.get('user_id')
    videos = GeneratedVideo.objects.filter(user=user_id)
    return render(request, 'video_list.html', {'videos': videos})

@custom_login_required
def delete_video(request, video_id):
    video = GeneratedVideo.objects.get(id=video_id)

    if video.video_file and os.path.isfile(video.video_file):
        os.remove(video.video_file)

    for tag in video.tags:
        tag.videos.remove(video)
        tag.save()

    video.delete()
    return redirect('list_videos')

@custom_login_required
def get_video(request, video_id):
    video = GeneratedVideo.objects.get(id=video_id)
    return render(request, 'video_detail.html', {'video': video})

@custom_login_required
def serve_video(request, video_id):
    try:
        video = GeneratedVideo.objects.get(id=video_id)
        # Directly serve a static file for testing
        file_path = video.video_file
        response = FileResponse(open(file_path, 'rb'), content_type='video/mp4')
        response['Content-Disposition'] = 'inline; filename="{}"'.format(video.name)
        return response
    except GeneratedVideo.DoesNotExist:
        return HttpResponse("Video not found", status=404)
