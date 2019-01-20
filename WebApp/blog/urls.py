from django.urls import path
from views import home

APP_NAME = 'blog'

urlpatterns = [
    path('', home, name='home')
]
