from django.urls import path
from .views import *


urlpatterns = [
    path('register/', register_page, name='user-register'),
    path('user-register-form/', registeration_form, name='user-register-form'),
    path('login/', login_page, name='user-login'),
    path('user-login-form/', login_form, name='user-login-form'),
    path('logout/', logout, name='user-logout'),
    path('profile/', profile_page, name='user-profile'),
    path('users/', user_list, name='user_list'),
    path('users/<int:pk>/toggle-status/', toggle_user_status, name='toggle_user_status'),
    path('users/<int:pk>/delete/', delete_user, name='delete_user'),
    path('api/otp/', get_otp, name='otp')
]   