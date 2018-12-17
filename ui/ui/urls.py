#from django.contrib import admin
from django.conf.urls import url, include
from rest_framework import routers
from jibarr import views

router = routers.DefaultRouter()

urlpatterns = [
    #path('Jibarr/', include('Jibarr.urls')),
    #path('mediafilesync/', include('Jibarr.urls')),
    #path('api/', include('api.urls')),

    url(r'^', include(router.urls)),
    #url(r'^', include('Jibarr.urls')),
    #url(r'^', views.index, name='index'),
    url(r'^jibarr/', include('jibarr.urls')),
    url(r'^Jibarr/', include('jibarr.urls')),
    url(r'^api/', include('api.urls')),
]
