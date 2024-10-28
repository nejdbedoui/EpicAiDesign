from django.shortcuts import render

import AlbumApp.models
import GalleryApp.models
import UserApp.models


# Create your views here.

def home_admin(request):
    return render(request, 'dashboard.html')


def user_list(request):
    users = UserApp.models.User.objects(role='user').all()
    return render(request, 'admin_users_list.html', {'users': users})


def gallery_list(request):
    gallerys = GalleryApp.models.ImageGallery.objects().all()
    return render(request, 'admin_gallery_list.html', {'gallerys': gallerys})


def album_list(request):
    albums = AlbumApp.models.MusicAlbum.objects().all()
    return render(request, 'admin_album_list.html', {'albums': albums})
