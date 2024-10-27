from django.urls import path
from . import views


urlpatterns = [
path('add_poem', views.Add_poem, name='add_poem'),
path('poeme/<str:id>/', views.Details_poeme, name='poemedetails'),
path('update/<str:id>/', views.update_poem, name='update_poem'),  # Utiliser le nom d'URL correct
path('delete/<str:id>/', views.delete_poem, name='delete_poem'),
path('poem/<str:id>/add-license/', views.add_license, name='add_license'),
path('licenses/', views.license_list, name='licenses'),  # Ajoutez cette ligne
    path('license/<str:id>/', views.license_details, name='license_details'),
path('licenses/delete/<str:id>/', views.delete_license, name='delete_license'),








]