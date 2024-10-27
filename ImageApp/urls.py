from django.urls import path
from . import views

urlpatterns = [
<<<<<<< HEAD
path('add_image', views.Add_image, name='add_image'),
=======
path('add_image', views.Generate_image, name='add_image'),
>>>>>>> 31048a1ab8292946577aeb18d50c15ac8b018416
]