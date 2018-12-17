from django.conf.urls import url, include
from rest_framework import routers
from django.urls import path

from jibarr import views

urlpatterns = [
    path('', views.index, name='index'),
    url(r'^profiles/', views.profiles, name='profiles'),
    url(r'^settings/', views.settings, name='settings'),
    url(r'^donate/', views.donate, name='donate'),
    url(r'^movies/', views.movies, name='movies'),
    url(r'^shows/', views.shows, name='shows'),
    url(r'^music/', views.music, name='music'),
    url(r'^runsync/', views.runsync, name='runsync')
]