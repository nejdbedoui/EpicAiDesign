# TagsApp/views.py
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import TagForm
from .models import Tag
from UserApp.models import User
from UserApp.decorator import custom_login_required

@custom_login_required
def tag_update(request, tag_id):
    tag = Tag.objects.get(id=tag_id)
    if request.method == 'POST':
        form = TagForm(request.POST)
        if form.is_valid():
            tag.name = form.cleaned_data['name']
            form.save()
            return redirect('tag_list')
    else:
        form = TagForm(initial={'name': tag.name})
    return render(request, 'tag_form.html', {'form': form})

@custom_login_required
def tag_delete(request, tag_id):
    tag = Tag.objects.get(id=tag_id)

    for video in tag.videos:
        video.tags.remove(tag)
        video.save()

    tag.delete()
    return redirect('list_videos')
