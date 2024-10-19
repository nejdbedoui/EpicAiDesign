from django.urls import path
from . import views

urlpatterns = [
path('add_poem', views.Add_poem, name='add_poem'),

]