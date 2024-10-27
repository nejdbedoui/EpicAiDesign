from django.urls import path
from . import views

urlpatterns = [
    path('add_reel', views.add_reel, name='add_reel'),

]
