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
    id = models.IntegerField(db_column='id', auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    profile_id = models.IntegerField()
    sonarr_id = models.IntegerField()
    lastRun = models.CharField(max_length=200)

    objects = models.Manager()

    class Meta:
        db_table = 'Jibarr_sonarr'
        
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
    rating = 0
    seasonCount = 0
    episodeCount = 0
    isNewer = False
    class Meta:
        managed = False