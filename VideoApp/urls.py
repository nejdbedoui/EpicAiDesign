from django.urls import path
from . import views

urlpatterns = [
    path('add/', views.add_video, name='add_video'),
    path('update/<str:video_id>/', views.update_video, name='update_video'),
    path('delete/<str:video_id>/', views.delete_video, name='delete_video'),
    path('mylist/', views.video_listUser, name='mylist_videos'),
    path('list/', views.video_list, name='list_videos'),
    path('detail/<str:video_id>/', views.get_video, name='get_video'),
    path('video/<str:video_id>/', views.serve_video, name='serve_video'),
]
