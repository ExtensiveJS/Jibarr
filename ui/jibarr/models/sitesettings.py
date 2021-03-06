import datetime
from django.db import models
from django.utils import timezone
from django.views.generic.detail import SingleObjectMixin
from django.views import View
import json
from rest_framework.views import APIView
from rest_framework.response import Response
from urllib.request import urlopen
from django.conf import settings
import urllib.request
from django.core.cache import cache


class SiteSettings(models.Model):
    id = models.IntegerField(db_column='Id', auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    radarr_enabled = models.IntegerField(db_column='RADARR_Enabled', null=False)
    radarr_path =  models.TextField(db_column='RADARR_Path')
    radarr_apikey = models.TextField(db_column='RADARR_APIKey')
    radarr_last_sync = models.TextField(db_column='RADARR_Last_Sync')
    sonarr_enabled = models.IntegerField(db_column='SONARR_Enabled', null=False)
    sonarr_path =  models.TextField(db_column='SONARR_Path')
    sonarr_apikey = models.TextField(db_column='SONARR_APIKey')
    sonarr_last_sync = models.TextField(db_column='SONARR_Last_Sync')
    lidarr_enabled = models.IntegerField(db_column='LIDARR_Enabled', null=False)
    lidarr_path =  models.TextField(db_column='LIDARR_Path')
    lidarr_apikey = models.TextField(db_column='LIDARR_APIKey')
    lidarr_last_sync = models.TextField(db_column='LIDARR_Last_Sync')
    jibarr_version = models.TextField(db_column='Jibarr_Version')
    scheduler_enabled = models.IntegerField(db_column='Scheduler_Enabled')
    upgrades_enabled = models.IntegerField(db_column="Upgrades_Enabled")
    objects = models.Manager()
    
    
    def checkVersion():

        # check if upgrades are enabled first.....
        sett = SiteSettings.objects.all()[:1].get()
        if sett.upgrades_enabled:
            "This does a version check against GitHub and the local system."
            newVersion = False
            CACHE_KEY_NEWVERSION = 'NEWVERSION'
            
            if cache.get(CACHE_KEY_NEWVERSION):
                newVersion = cache.get(CACHE_KEY_NEWVERSION)
            else:
                
                jv = sett.jibarr_version
                # https://github.com/ExtensiveJS/Jibarr/wiki/Current-Versions
                try:
                    resp = urllib.request.urlopen('https://github.com/ExtensiveJS/Jibarr/wiki/Current-Versions')
                    html = resp.read()
                    htmlstr = html.decode('utf8')
                    htmlSplit = htmlstr.split("\n")
                    for line in htmlSplit:
                        if line.find('Jibarr_Version') > -1:
                            jv = line.replace("</p>","").replace("<p>","").replace("Jibarr_Code: ", "").replace("<br>","")
                    resp.close()
                except:
                    pass
                
                
                if(jv != sett.jibarr_version):
                    newVersion = True
                cache.set(CACHE_KEY_NEWVERSION,newVersion)
        else:
            newVersion = False
        return newVersion

    
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

