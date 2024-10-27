from django.urls import path
from . import views

urlpatterns = [
    path('add_reel', views.add_reel, name='add_reel'),
    path('Reels_Show', views.reels_show, name='Reels_Show')

]
