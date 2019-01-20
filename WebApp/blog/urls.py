from django.urls import path
from .views import home, compose

APP_NAME = 'blog'

urlpatterns = [
    path('', home, name='blog-home'),
    path('create/', compose, name='blog-compose')
]
