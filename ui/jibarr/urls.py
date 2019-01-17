from django.conf.urls import url, include
from rest_framework import routers
from django.urls import path

from jibarr import views

urlpatterns = [
    path('', views.index, name='index'),
    url(r'^profiles/', views.profiles, name='profiles'),
    url(r'^sitesettings/', views.sitesettings, name='sitesettings'),
    url(r'^donate/', views.donate, name='donate'),
    url(r'^movies/', views.movies, name='movies'),
    url(r'^shows/', views.shows, name='shows'),
    url(r'^music/', views.music, name='music'),
    url(r'^runsync/', views.runsync, name='runsync'),
    url(r'^logs/', views.logs, name='logs'),
    url(r'^about/', views.about, name='about'),
    url(r'^updates/', views.updates, name='updates'),
    url(r'systemsettings/', views.systemsettings, name='systemsettings'),
    url(r'upgrade/', views.upgrade, name='upgrade')
]