import datetime
from django.db import models
from django.utils import timezone
from django.views.generic.detail import SingleObjectMixin
from django.views import View
import json
from rest_framework.views import APIView
from rest_framework.response import Response
from urllib.request import urlopen

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

    objects = models.Manager()

    class Meta:
        managed = False
        db_table = 'Jibarr_settings' 

class PageStuff(object):
    # properties here
    pageNumber = 0
    totalPages = 0
    perPage = 5
    totalRecords = 0
    class Meta:
        managed = False