from django.contrib import admin
from django.urls import path, include

from UserApp import views as Userviews

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', Userviews.home, name='home'),
    path('admin/', admin.site.urls),
    path('users/', include('django.contrib.auth.urls')),
    path('users/', include('UserApp.urls')),
    path('speech/', include('SpeechApp.urls')),
    path('image/', include('ImageApp.urls')),
    path('music/', include('MusicApp.urls')),
    path('poem/', include('PoemApp.urls')),
    path('video/', include('VideoApp.urls')),
    path('tagsVideo/', include('TagsVideoApp.urls')),
    path('Album/', include('AlbumApp.urls')),
    path('Gallery/', include('GalleryApp.urls')),
    path('Blog/', include('BlogSpeechApp.urls')),
    path('Reel/', include('ReelApp.urls')),
]
if settings.DEBUG is True:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
