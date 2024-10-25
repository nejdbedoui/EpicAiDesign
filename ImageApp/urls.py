from django.urls import path
from . import views

urlpatterns = [
path('add_image', views.Add_image, name='add_image'),
]