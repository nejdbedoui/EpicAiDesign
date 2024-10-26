from django.urls import path
from . import views

urlpatterns = [
    path('addAlbum', views.add_album, name='addAlbum'),
    path('add_to_Album', views.add_to_Album, name='add_to_Album'),
    path('my_albums', views.my_albums, name='my_albums'),
    path('<str:id>/', views.album_tracks, name='album_tracks'),
]
