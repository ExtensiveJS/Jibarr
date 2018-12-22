import datetime
from django.db import models
from django.utils import timezone
from django.views.generic.detail import SingleObjectMixin
from django.views import View
import json
from rest_framework.views import APIView
from rest_framework.response import Response
from urllib.request import urlopen

class ProfileLidarr(models.Model):
    id = models.IntegerField(db_column='id', auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    profile_id = models.IntegerField()
    lidarr_id = models.IntegerField()
    lastRun = models.CharField(max_length=200)
    class Meta:
        db_table = 'Jibarr_lidarr'