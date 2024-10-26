from datetime import datetime

from django.contrib import messages
from django.shortcuts import render, redirect

import MusicApp.models
import UserApp.models
from AlbumApp.models import MusicAlbum


# Create your views here.
def add_album(request):
    category = request.POST.get('category')
    sort = request.POST.get('sort')
    data = MusicApp.models.MusicArt.objects.all().order_by(f"-{sort}")
    if sort is None:
        sort = 'created_at'
    if category is None:
        category = 'Music'

    if request.method == 'POST':
        title = request.POST.get('title')
        cover = request.FILES.get('cover')
        if title is None:
            messages.error(request, "Title Is Required")
            if cover is None:
                messages.error(request, "Image Is Required")
            return redirect('Gallery')
        user = UserApp.models.User.objects.get(email=request.session['user_email'])
        album = MusicAlbum(
            title=title,
            cover=cover,
            rating=0,
            created_at=datetime.now(),
            user=user
        )
        album.save()
        messages.success(request, 'Album added successfully!')
        return redirect('Gallery')


def add_to_Album(request):
    album_id = request.POST.get('selected_album')
    album = MusicAlbum.objects(id=album_id).first()
    music_art_id = request.POST.get('music_art_id')
    music_art = MusicApp.models.MusicArt.objects(id=music_art_id).first()
    if album and music_art:
        if music_art not in album.tracks:
            album.tracks.append(music_art)
            album.save()
            messages.success(request, 'Music added to album successfully!')
        else:
            messages.error(request, 'Music Alredy Exist.')
    else:
        messages.error(request, 'Album or Music Art not found.')
    return redirect('Gallery')


def my_albums(request):
    user = UserApp.models.User.objects.get(email=request.session['user_email'])
    albums = MusicAlbum.objects(user=user).all().order_by('created_at')
    return render(request, 'my_albums.html', {'albums': albums})
