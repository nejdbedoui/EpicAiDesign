from django.contrib import admin
from django.urls import path, include

from UserApp import views as Userviews

urlpatterns = [
    path('', Userviews.home, name='home'),
    path('admin/', admin.site.urls),
    path('users/', include('django.contrib.auth.urls')),
    path('users/', include('UserApp.urls')),
    path('animation/', include('SpeechApp.urls')),
    path('image/', include('ImageApp.urls')),
    path('music/', include('MusicApp.urls')),
    path('poem/', include('PoemApp.urls')),
    path('video/', include('VideoApp.urls')),
]
