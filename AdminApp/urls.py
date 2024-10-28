from django.urls import path
from . import views

urlpatterns = [
    path('Dashboard', views.home_admin, name='dashboard'),
    path('Users', views.user_list, name='admin_users'),
    path('Gallery', views.gallery_list, name='admin_Gallery'),
    path('Albums', views.album_list, name='admin_Albums'),
]
