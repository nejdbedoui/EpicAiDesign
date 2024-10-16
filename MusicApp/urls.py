from django.urls import path
from . import views

urlpatterns = [
    path('add_music', views.Add_music, name='add_music'),
]
