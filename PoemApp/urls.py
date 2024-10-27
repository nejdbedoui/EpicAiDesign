from django.urls import path
from . import views


urlpatterns = [
path('add_poem', views.Add_poem, name='add_poem'),
path('poeme/<str:id>/', views.Details_poeme, name='poemedetails'),
path('update/<str:id>/', views.update_poem, name='update_poem'),  # Utiliser le nom d'URL correct
path('delete/<str:id>/', views.delete_poem, name='delete_poem'),





]