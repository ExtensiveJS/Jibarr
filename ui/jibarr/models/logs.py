import datetime
from django.db import models
from django.utils import timezone
from django.views.generic.detail import SingleObjectMixin
from django.views import View
import json
from rest_framework.views import APIView
from rest_framework.response import Response
from urllib.request import urlopen

class Logs(models.Model):
    id = models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    log_type = models.CharField(max_length=25)
    log_message = models.CharField(max_length=2000)
    log_datetime = models.CharField(max_length=200)
    log_category = models.CharField(max_length=25)
    objects = models.Manager()
    class Meta:
        db_table = 'Jibarr_logs'