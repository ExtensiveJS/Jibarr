from django.conf.urls import url, include
from rest_framework import routers
from api import views

router = routers.DefaultRouter()
router.register(r'settings', views.SettingsViewSet)
router.register(r'profile', views.ProfileViewSet)
router.register(r'profileradarr', views.ProfileRadarrViewSet)
router.register(r'profilesonarr', views.ProfileSonarrViewSet)
router.register(r'profilelidarr', views.ProfileLidarrViewSet)
router.register(r'logs', views.LogsViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    url(r'^runsync/', views.RunSync),
    url(r'^GetFolders/', views.GetFolders),
    url(r'^', include(router.urls)),
]