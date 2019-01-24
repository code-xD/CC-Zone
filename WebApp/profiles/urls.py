from django.urls import path
from .views import home, create, my_post

APP_NAME = 'profile'

urlpatterns = [
    path('<username>', home, name='profile-home'),
    path('create/', create, name='profile-create'),
    path('posts/<int:pk>', my_post, name='profile-posts')
]
