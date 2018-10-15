from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('mediafilesync', views.index, name='mediafilesync'),
    path('SyncProcessor', views.syncprocessor, name='syncprocessor'),
    path('Simulated', views.simulated, name='simulated'),
    path('runsimulated', views.runsimulated, name='runsimulated')
]