from django.urls import path
from . import views

urlpatterns = [
path('image', views.Generate_image, name='add_image'),
]