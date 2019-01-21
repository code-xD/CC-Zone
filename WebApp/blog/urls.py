from django.urls import path
from .views import home, compose, detail

APP_NAME = 'blog'

urlpatterns = [
    path('', home, name='blog-home'),
    path('create/', compose, name='blog-compose'),
    path('detail/<int:pk>/', detail, name='blog-detail'),
]
