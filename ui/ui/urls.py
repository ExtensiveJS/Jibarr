#from django.contrib import admin
from django.conf.urls import url, include
from rest_framework import routers
from MediaFileSync import views

router = routers.DefaultRouter()

urlpatterns = [
    #path('MediaFileSync/', include('MediaFileSync.urls')),
    #path('mediafilesync/', include('MediaFileSync.urls')),
    #path('api/', include('api.urls')),

    url(r'^', include(router.urls)),
    #url(r'^', include('MediaFileSync.urls')),
    #url(r'^', views.index, name='index'),
    url(r'^mediafilesync/', include('MediaFileSync.urls')),
    url(r'^MediaFileSync/', include('MediaFileSync.urls')),
    url(r'^api/', include('api.urls')),
]
