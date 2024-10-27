from django.urls import path
from . import views

urlpatterns = [
    path('add/', views.add_speech, name='add_speech'),
    path('update/<str:speech_id>/', views.update_speech, name='update_speech'),
    path('delete/<str:speech_id>/', views.delete_speech, name='delete_speech'),
    path('mylist/', views.speech_listUser, name='mylist_speechs'),
    path('list/', views.speech_list, name='list_speechs'),
    path('detail/<str:speech_id>/', views.get_speech, name='get_speech'),
    path('audio/<str:speech_id>/', views.serve_audio, name='serve_audio'),
]
