from django.conf.urls import url, include
from rest_framework import routers
from jibarr import views

router = routers.DefaultRouter()

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^jibarr/', include('jibarr.urls')),
    url(r'^Jibarr/', include('jibarr.urls')),
    url(r'^api/', include('api.urls')),
]
