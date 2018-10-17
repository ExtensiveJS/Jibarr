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
    path('runsimulated', views.runsimulated, name='runsimulated')
]