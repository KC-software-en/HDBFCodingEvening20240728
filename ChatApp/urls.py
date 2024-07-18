from django.urls import path, include
# import views
from . import views

# set a path to the index function in views.py
urlpatterns = [
path('', views.index),
]
