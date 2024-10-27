from django.urls import path
from . import views


urlpatterns = [
path('add_poem', views.Add_poem, name='add_poem'),
<<<<<<< HEAD
=======
path('poeme/<str:id>/', views.Details_poeme, name='poemedetails'),
path('update/<str:id>/', views.update_poem, name='update_poem'),  # Utiliser le nom d'URL correct
path('delete/<str:id>/', views.delete_poem, name='delete_poem'),




>>>>>>> 31048a1ab8292946577aeb18d50c15ac8b018416

]