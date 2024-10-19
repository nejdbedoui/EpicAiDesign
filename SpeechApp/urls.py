from django.urls import path
from . import views

urlpatterns = [
path('add_speech', views.Add_speech, name='add_speech'),
]
