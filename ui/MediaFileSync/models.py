import datetime
from django.db import models
from django.utils import timezone
from django.views.generic.detail import SingleObjectMixin
from django.views import View
import json
from rest_framework.views import APIView
from rest_framework.response import Response
from urllib.request import urlopen

# Create your models here.

#class Media(models.Model):
#    media_id = models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
#    media_source = models.CharField(max_length=200)
#    media_source_id = models.IntegerField()
#    media_lastUpd = models.DateTimeField()
#    #def was_updated_recently(self):
#    #    return self.media_lastUpd >= timezone.now() - datetime.timedelta(days=1)

class Profile(models.Model):
    id = models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    profile_name = models.CharField(max_length=200)
    profile_lastRun = models.CharField(max_length=200)

class Settings(models.Model):
    id = models.IntegerField(db_column='Id', auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    radarr_enabled = models.IntegerField(db_column='RADARR_Enabled', null=False)
    radarr_path =  models.TextField(db_column='RADARR_Path')
    radarr_apikey = models.TextField(db_column='RADARR_APIKey')
    sonarr_enabled = models.IntegerField(db_column='SONARR_Enabled', null=False)
    sonarr_path =  models.TextField(db_column='SONARR_Path')
    sonarr_apikey = models.TextField(db_column='SONARR_APIKey')
    lidarr_enabled = models.IntegerField(db_column='LIDARR_Enabled', null=False)
    lidarr_path =  models.TextField(db_column='LIDARR_Path')
    lidarr_apikey = models.TextField(db_column='LIDARR_APIKey')
    class Meta:
        managed = False
        db_table = 'MediaFileSync_settings'  

class radarrMovieList(list):
     movielist = []
     def __init__(self):
        self.movielist = []

class radarrMovie(object):
    # properties here
    r_id = 0
    media_id = 0
    title = ""
    tmdbid = ""
    releaseDate = ""
    lastUpdt = ""
    folderName = ""
    fileName = ""
    isMonitored = False
    isNewer = False
    rating = 0
    class Meta:
        managed = False

class sonarrShowList(list):
    showlist = []
    def __init__(self):
        self.showlist = []

class sonarrShow(object):
    s_id = 0 # id
    media_id = 0 # from MFS
    title = "" # title
    year = "" # year
    imdbId = 0 # imdbId
    tvdbId = 0 # tvdbId
    tvRageId = 0 # tvRageId
    status = "unknown"
    folderName = "" # path
    isMonitored = False
    class Meta:
        managed = False

class ProfileRadarr(models.Model):
    id = models.IntegerField(db_column='id', auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    profile_id = models.IntegerField()
    radarr_id = models.IntegerField()
    lastRun = models.CharField(max_length=200)
    class Meta:
        db_table = 'MediaFileSync_radarr'

class ProfileSonarr(models.Model):
    id = models.IntegerField(db_column='id', auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    profile_id = models.IntegerField()
    sonarr_id = models.IntegerField()
    lastRun = models.CharField(max_length=200)
    class Meta:
        db_table = 'MediaFileSync_sonarr'

class ProfileLidarr(models.Model):
    id = models.IntegerField(db_column='id', auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    profile_id = models.IntegerField()
    lidarr_id = models.IntegerField()
    lastRun = models.CharField(max_length=200)
    class Meta:
        db_table = 'MediaFileSync_lidarr'