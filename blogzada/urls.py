from django.urls import path, include
from .views import index, register_user, login_user, logout_user, create_post, save_data

app_name = 'blogzada'

urlpatterns = [
    path('', index, name='index'),
    path('register/', register_user, name='register'),
    path('login/', login_user, name='login'),
    path('logout/', logout_user, name='logout'),
    path('create_post/', create_post, name='create_post'),
    path('save_data/', save_data, name='save_data'),
]
