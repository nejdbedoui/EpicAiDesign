from django.urls import path
from . import views

urlpatterns = [
    path('delete_tag/<str:tag_id>/', views.tag_delete, name='delete_tag'),
]
