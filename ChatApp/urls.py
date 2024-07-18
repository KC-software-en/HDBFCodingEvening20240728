from django.urls import path, include
# import views
from . import views

# set a path to the index function in views.py
# add a name for the index view
urlpatterns = [
path('', views.index, name="index"),
]
