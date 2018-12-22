import datetime
from django.db import models
from django.utils import timezone
from django.views.generic.detail import SingleObjectMixin
from django.views import View
import json
from rest_framework.views import APIView
from rest_framework.response import Response
from urllib.request import urlopen

class ProfileRadarr(models.Model):
    profile_id = models.IntegerField()
    radarr_id = models.IntegerField()
    lastRun = models.CharField(max_length=200)

    objects = models.Manager()
    
    class Meta:
        db_table = 'Jibarr_radarr'
        
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