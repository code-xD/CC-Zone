from django.urls import path
from .views import home, compose, detail, update_post, delete_post

APP_NAME = 'blog'

urlpatterns = [
    path('', home, name='blog-home'),
    path('create/', compose, name='blog-compose'),
    path('detail/<int:pk>/', detail, name='blog-detail'),
    path('update/<int:pk>/', update_post, name='blog-update'),
    path('delete/<int:pk>/', delete_post, name='blog-delete')
]
