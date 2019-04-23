import datetime
from django.db import models
from django.utils import timezone
from django.views.generic.detail import SingleObjectMixin
from django.views import View
import json
from rest_framework.views import APIView
from rest_framework.response import Response
from urllib.request import urlopen

class Profile(models.Model):
    id = models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    profile_name = models.CharField(max_length=200)
    profile_lastRun = models.CharField(max_length=200)
    profile_lastPath = models.CharField(max_length=512)
    radarr_lastRun = models.CharField(max_length=200)
    radarr_monitor = models.IntegerField(null=False)
    sonarr_monitor = models.IntegerField(null=False)
    sonarr_lastRun = models.CharField(max_length=200)
    objects = models.Manager()