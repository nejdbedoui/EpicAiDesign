from django.urls import path
from . import views

urlpatterns = [
path('add_video', views.Add_Video, name='add_video'),
]