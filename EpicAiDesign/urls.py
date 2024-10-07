from django.contrib import admin
from django.urls import path, include

from UserApp import views as Userviews

urlpatterns = [
    path('', Userviews.home, name='home'),
    path('admin/', admin.site.urls),
    path('users/', include('django.contrib.auth.urls')),
    path('users/', include('UserApp.urls')),
]
