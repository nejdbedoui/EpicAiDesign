from django.urls import path
from . import views

urlpatterns = [
    path('add/<str:speech_id>', views.add_blog, name='add_blog'),
    path('delete/<str:blog_id>', views.delete_blog, name='delete_blog'),
]
