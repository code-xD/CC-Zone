from django.urls import path
from .views import home, create, my_post, base_create

APP_NAME = 'profile'

urlpatterns = [
    path('<username>', home, name='profile-home'),
    path('create/', create, name='profile-create'),
    path('first_create/', base_create, name='profile-base-create'),
    path('posts/<int:pk>', my_post, name='profile-posts')
    # path('create/', compose, name='blog-compose'),
    # path('detail/<int:pk>/', detail, name='blog-detail'),
]
