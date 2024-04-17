# pages/urls.py
from django.urls import path

from .views import objects, home

urlpatterns = [
    path("", home, name="home"),
    path("objects", objects, name="objects")
]