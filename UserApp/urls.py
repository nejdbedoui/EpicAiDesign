from django.urls import path
from . import views

urlpatterns = [
    path('login', views.user_login, name='login'),
    path('signup', views.signup, name='signup'),
    path('profile', views.profile, name='profile'),
    path('profile/info/', views.personalInfo, name='userInfo'),
    path('logout', views.logout_user, name='logout'),
    path('verifyEmail', views.verifyEmail, name='verify_email'),
    path('resetPassword', views.reset_password, name='resetPassword'),
    path('reset_password', views.reset_password_view, name='reset_password'),
    path('profile/editProfile/', views.editProfile, name='editProfile'),
    path('user_list', views.user_list, name='user_list'),
    path('Gallery',views.gallery,name='Gallery'),
]
