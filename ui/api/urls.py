from django.conf.urls import url, include
from rest_framework import routers
from api import views

router = routers.DefaultRouter()
router.register(r'sitesettings', views.SiteSettingsViewSet)
router.register(r'profile', views.ProfileViewSet)
router.register(r'profileradarr', views.ProfileRadarrViewSet)
router.register(r'profilesonarr', views.ProfileSonarrViewSet)
router.register(r'profilelidarr', views.ProfileLidarrViewSet)
router.register(r'logs', views.LogsViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    url(r'^runsync/', views.RunSync),
    url(r'^runsyncshows/', views.RunSyncShows),
    url(r'^GetFolders/', views.GetFolders),
    url(r'dbsync', views.dbsync),
    url(r'scheduler',views.scheduler),
    url(r'marksynced', views.marksynced),
    url(r'markshowssynced', views.markshowssynced),
    url(r'runUpgradeProcess/', views.runUpgradeProcess),
    url(r'upgrades',views.upgrades),
    url(r'automonitor',views.automonitor),
    url(r'markmoviesmonitored/',views.markmoviesmonitored),
    url(r'changeRadarrStatus/',views.changeRadarrStatus),
    url(r'changeSonarrStatus/',views.changeSonarrStatus),
    url(r'skipEpisode/',views.skipEpisode),
    url(r'runbackup/',views.runbackup),
    url(r'changesSeasonExclude/',views.changesSeasonExclude),
    url(r'^', include(router.urls))
]