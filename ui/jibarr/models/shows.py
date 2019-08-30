import datetime
from django.db import models
from django.utils import timezone
from django.views.generic.detail import SingleObjectMixin
from django.views import View
import json
from rest_framework.views import APIView
from rest_framework.response import Response
from urllib.request import urlopen

class ProfileSonarr(models.Model):
    profile_id = models.IntegerField()
    sonarr_id = models.IntegerField()
    lastRun = models.CharField(max_length=200)

    objects = models.Manager()

    class Meta:
        db_table = 'Profile_Sonarr_Show'

class ProfileSonarrEpisode(models.Model):
    profile_id = models.IntegerField()
    sonarr_id = models.IntegerField()
    lastRun = models.CharField(max_length=200)

    objects = models.Manager()

    class Meta:
        db_table = 'Profile_Sonarr_Episode'
        
class sonarrShowList(list):
    showlist = []
    def __init__(self):
        self.showlist = []

class sonarrShow(object):
    # properties here
    id = 0
    sonarr_id = 0
    title = ""
    title_slug = ""
    year = ""
    path = ""
    lastInfoSync = ""
    rating = 0
    tvdbId = ""
    tvRageId = ""
    tvMazeId = ""
    imdbId = ""
    seasonCount = 0
    episodeCount = 0
    episodeFileCount = 0
    description = ""
    isMonitored = False
    status = ""

    class Meta:
        managed = False

class SonarrShowMedia(models.Model):
    sonarr_id = models.IntegerField()
    title = models.CharField(max_length=200)
    title_slug = models.CharField(max_length=200)
    year = models.CharField(max_length=200)
    path = models.CharField(max_length=200)
    lastInfoSync = models.CharField(max_length=200)
    rating = models.CharField(max_length=10)
    tvdbId = models.CharField(max_length=200)
    tvRageId = models.CharField(max_length=200)
    tvMazeId = models.CharField(max_length=200)
    imdbId = models.CharField(max_length=200)
    seasonCount = models.IntegerField()
    episodeCount = models.IntegerField()
    episodeFileCount = models.IntegerField()
    description = models.CharField(max_length=1000)
    status = models.CharField(max_length=20)

    objects = models.Manager()

    class Meta:
        db_table = 'Jibarr_Sonarr_Show'

class SonarrEpisodeMedia(models.Model):
    sonarr_id = models.IntegerField()
    seriesId = models.IntegerField()
    episodeNumber = models.IntegerField()
    title = models.CharField(max_length=200)
    seasonNumber = models.IntegerField()
    path = models.CharField(max_length=200)
    dateAdded = models.CharField(max_length=200)
    quality = models.CharField(max_length=200)
    description = models.CharField(max_length=2000)
    airDate = models.CharField(max_length=200)
    size = models.IntegerField()

    objects = models.Manager()

    class Meta:
        db_table = 'Jibarr_Sonarr_Episode'

class sonarrEpisode(object):
    id = 0
    sonarr_id = 0
    seriesId = 0
    episodeNumber = 0
    title = ""
    seasonNumber = 0
    path = ""
    dateAdded = ""
    quality = ""
    description = ""
    airDate = ""
    size = 0
    isMonitored = False
    isNewer = False

    class Meta:
        managed = False

class sonarrSeason(object):
    title = ''
    episodes = [SonarrEpisodeMedia]
    # default seasons to isMonitored = True
    isMonitored = True

    class Meta:
        managed = False

class sonarrEpisodeList(list):
    episodelist = []
    def __init__(self):
        self.episodelist = []

class SonarrSeasonExclusions(models.Model):
    series_id = models.IntegerField()
    seasonNumber = models.IntegerField()
    profile_id = models.IntegerField()

    objects = models.Manager()

    class Meta:
        db_table = 'Profile_Sonarr_Season_Exclude'