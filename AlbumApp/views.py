from datetime import datetime

from bson import ObjectId
from django.contrib import messages
from django.shortcuts import render, redirect

import MusicApp.models
import UserApp.models
from AlbumApp.models import MusicAlbum, UserRating


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
        description = request.POST.get('description')
        if title is None or title.strip() == "":
            messages.error(request, "Title is required.")
        if cover is None:
            messages.error(request, "Image is required.")
        if description is None or description.strip() == "":
            messages.error(request, "Description is required.")

        if messages.get_messages(request):
            return redirect('Gallery')

        user = UserApp.models.User.objects.get(email=request.session['user_email'])
        album = MusicAlbum(
            title=title,
            cover=cover,
            description=description,
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
    if request.method == 'POST':
        album_id = request.POST.get('id_album')
        album_to_delete = MusicAlbum.objects.get(id=album_id)
        album_to_delete.delete()
    return render(request, 'my_albums.html', {'albums': albums})


def album_tracks(request, id):
    album = MusicAlbum.objects(id=id).first()
    if request.method == 'POST':
        id_music = request.POST.get('id_music')
        music = MusicApp.models.MusicArt.objects(id=id_music).first()
        if music in album.tracks:
            album.tracks.remove(music)
            album.save()
            messages.success(request, "Track Removed From Album")
        messages.error(request, "Track Not Found")
    return render(request, 'album_tracks.html', {'album': album})


def albums_show(request):
    albums = MusicAlbum.objects.all().order_by('-rating')
    if request.method == 'POST':
        rating = float(request.POST.get('rating'))
        album_id = request.POST.get('id')
        user = UserApp.models.User.objects.get(email=request.session['user_email'])
        album = MusicAlbum.objects(id=album_id).first()
        user_rating_instance = None
        for user_rating in album.user_rated:
            if user_rating.user == user:
                user_rating_instance = user_rating
                break
        if user_rating_instance:
            user_rating_instance.rating = rating
        else:
            user_rating_instance = UserRating(user=user, rating=rating)
            album.user_rated.append(user_rating_instance)
        album.save()
        total_ratings = sum(user_rating.rating for user_rating in album.user_rated)
        average_rating = total_ratings / len(album.user_rated) if album.user_rated else 0
        album.rating = average_rating
        album.save()
        return render(request, 'albums_show.html', {'albums': albums, 'message': 'Rating submitted successfully!'})

    return render(request, 'albums_show.html', {'albums': albums})
