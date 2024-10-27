from django.urls import path
from . import views
urlpatterns = [
    path('add_gallery', views.add_gallery, name='add_gallery'),
    path('add_to_gallery/<str:id>/', views.add_to_gallery, name='add_to_gallery'),
    path('my_galleries', views.my_galleries, name='my_galleries'),
    path('add_img_to_gallery', views.add_img_to_gallery, name='add_img_to_gallery'),
]
