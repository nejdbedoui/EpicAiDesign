from django.urls import path
from . import views

urlpatterns = [
    path('', views.user_list, name='users_list'),
    path('login', views.user_login, name='login'),
    path('signup', views.signup, name='signup'),
    path('profile', views.profile, name='profile'),
    path('profile/info/', views.personalInfo, name='userInfo'),
    path('logout', views.logout_user, name='logout'),
    path('verifyEmail', views.verifyEmail, name='verify_email'),
]
