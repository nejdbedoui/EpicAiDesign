from django.urls import path
from . import views

urlpatterns = [
    path('music', views.Generate_music, name='music'),
]
