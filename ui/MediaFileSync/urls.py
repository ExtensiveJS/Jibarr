from django.conf.urls import url, include
#from django.urls import path
from rest_framework import routers
from django.urls import path

from . import views
# profiles
# settings
# dontate
urlpatterns = [
    path('', views.index, name='index'),
    #path('SyncProcessor', views.syncprocessor, name='syncprocessor'),
    #path('Simulated', views.simulated, name='simulated'),
    #path('runsimulated', views.runsimulated, name='runsimulated'),
    #path('profiles', views.profiles, name='profiles'),
    #path('settings', views.settings, name='settings'),
    #path('donate', views.donate, name='donate'),

    url(r'^syncprocessor/', views.syncprocessor, name='syncprocessor'),
    url(r'^simulated/', views.simulated, name='simulated'),
    url(r'^runsimulated/', views.runsimulated, name='runsimulated'),
    url(r'^profiles/', views.profiles, name='profiles'),
    url(r'^settings/', views.settings, name='settings'),
    url(r'^donate/', views.donate, name='donate'),
    url(r'^movies/', views.movies, name='movies'),
    #url(r'^', views.index, name='index'),
    
]