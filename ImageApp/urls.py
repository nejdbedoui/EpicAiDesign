from django.urls import path
from . import views

urlpatterns = [
path('add_image', views.Generate_image, name='add_image'),
]