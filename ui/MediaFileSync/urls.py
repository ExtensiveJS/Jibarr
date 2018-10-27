from django.urls import path

from . import views
# profiles
# settings
# dontate
urlpatterns = [
    path('', views.index, name='index'),
    #path('MediaFileSync', views.index, name='mediafilesync'),
    path('SyncProcessor', views.syncprocessor, name='syncprocessor'),
    path('Simulated', views.simulated, name='simulated'),
    path('runsimulated', views.runsimulated, name='runsimulated'),
    path('profiles', views.profiles, name='profiles'),
    path('settings', views.settings, name='settings'),
    path('donate', views.donate, name='donate')
]