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

class Media(models.Model):
    media_id = models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    media_source = models.CharField(max_length=200)
    media_source_id = models.IntegerField()
    media_lastUpd = models.DateTimeField()
    #def __str__(self):
    #    return self.question_text
    def was_updated_recently(self):
        return self.media_lastUpd >= timezone.now() - datetime.timedelta(days=1)

class Profile(models.Model):
    id = models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    profile_name = models.CharField(max_length=200)
    profile_lastRun = models.CharField(max_length=200)

class ProfileMedia(models.Model):
    profilemedia_id = models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    profile_id = models.IntegerField()
    media_id = models.IntegerField()

class Settings(models.Model):
    id = models.IntegerField(db_column='Id', auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    radarr_enabled = models.IntegerField(db_column='RADARR_Enabled', null=False)
    radarr_path =  models.TextField(db_column='RADARR_Path')
    radarr_apikey = models.TextField(db_column='RADARR_APIKey')
    sonarr_enabled = models.IntegerField(db_column='SONARR_Enabled', null=False)
    sonarr_path =  models.TextField(db_column='SONARR_Path')
    lidarr_enabled = models.IntegerField(db_column='LIDARR_Enabled', null=False)
    lidarr_path =  models.TextField(db_column='LIDARR_Path')
    class Meta:
        managed = False
        db_table = 'MediaFileSync_settings'

#class mfsMovie(object):
#    media_id = 0
#    title = ""
#    tmdbid = ""
#    releaseDate = ""
#    lastUpdt = ""
#    isMonitored = False
#    isNewer = False
#    class Meta:
#        managed = False
#    def new(self):
#        self.media_id = 0
#        self.title = ""
#        self.tmdbid = ""
#        self.releaseDate = ""
#        self.lastUpdt = ""
#        self.isMonitored = False
#        self.isNewer = False
#        return(self)
#    def __init__(self):
#        self.media_id = 0
#        self.title = ""
#        self.tmdbid = ""
#        self.releaseDate = ""
#        self.lastUpdt = ""
#        self.isMonitored = False
#        self.isNewer = False    

class radarrMovieList(list):
    movielist = []
    count = 0
    class Meta:
        managed = False
    def __init__(self):
        data = urlopen("http://localhost:7878/api/movie?apikey=7b8c09c2a62b4cc6917be34043f67313").read()
        output = json.loads(data)
        self.movielist = []
        cnt = 0
        for var in output:
            cnt = cnt + 1
            rm = radarrMovie()
            rm.title = var['title']
            rm.r_id = var['id']

            try:
                rm.releaseDate = var['inCinemas']
            except KeyError:
                pass
                     
            if var['hasFile']:
                rm.lastUpdt = var['movieFile']['dateAdded']
                rm.folderName = var["folderName"]
                rm.fileName =  var["movieFile"]["relativePath"]
          
            #pm_list = ProfileMedia.objects.all()
            #for val2 in pm_list:
            #    if val2.profile_id == 1:
            #        if val2.media_source_id == var.r_id:
            #            rm.isMonitored = True
                        

            rm.media_id = var['id']
            rm.isNewer = False
            self.movielist.append(rm)
        self.count = cnt

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
    class Meta:
        managed = False
    #def __init__(self):
    #    data = urlopen("http://localhost:7878/api/movie?apikey=7b8c09c2a62b4cc6917be34043f67313").read()
    #    output = json.loads(data)
    #    #self.r_id = output[1].id
     #   self.title = "qwer" #output[1]['title']
    #    #self.inCinemas = output[1].inCinemas
    #    #self.dateAdded = output[1].movieFile.dateAdded
        
        