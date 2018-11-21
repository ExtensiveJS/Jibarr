import time
import types
import json
from time import mktime
from datetime import datetime
from dateutil.parser import parser
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from urllib.request import urlopen
import MediaFileSync.checkFolder
from .models import Settings, radarrMovie, radarrMovieList, Profile, ProfileRadarr

def index(request):
    media_list = [] 
    #radarr_list = Movies.objects.using("radarr").all()
    system_settings = Settings.objects.all()[:1].get()
    filtered_list = []

    #for val in radarr_list:
    #    for val2 in media_list:
    #        if val.id == val2.media_id:
    #            filtered_list.append(val)


    context = {
        'media_list': media_list,
        #'radarr_list': radarr_list,
        'filtered_list': filtered_list,
        'system_settings': system_settings
    }
    template = loader.get_template("MediaFileSync/index.html")
    return HttpResponse(template.render(context, request))

def profiles(request):
    system_settings = Settings.objects.all()[:1].get()
    profile_list = Profile.objects.all()
    context = {
        'system_settings': system_settings,
        'profile_list': profile_list
    }
    template = loader.get_template("MediaFileSync/profiles.html")
    return HttpResponse(template.render(context, request))

def settings(request):
    system_settings = Settings.objects.all()[:1].get()
    context = {
        'system_settings': system_settings
    }
    template = loader.get_template("MediaFileSync/settings.html")
    return HttpResponse(template.render(context, request))

def donate(request):
    system_settings = Settings.objects.all()[:1].get()
    context = {
        'system_settings': system_settings
    }
    template = loader.get_template("MediaFileSync/donate.html")
    return HttpResponse(template.render(context, request))

def movies(request):
    system_settings = Settings.objects.all()[:1].get()
    prof = Profile.objects.get(id=1)
    rML = radarrMovieList()
    rML.movielist.clear
    prList = ProfileRadarr.objects.filter(profile_id=prof.id)
    data = urlopen(system_settings.radarr_path + "/api/movie?apikey=" + system_settings.radarr_apikey).read()
    output = json.loads(data)
    cnt = 0
    monCnt = 0
    monSync = 0
    monNotSync = 0
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
            rm.size = var["movieFile"]["size"]
        
        rm.rating = var["ratings"]["value"]

        try:
            rm.tmdbid = var["tmdbId"]
        except KeyError:
            pass
        
        try:
            rm.imdbid = var["imdbId"]
        except KeyError:
            pass
        
        # find the media_id from the Media table
        for pr in prList:
            if pr.radarr_id == var["id"]:
                rm.media_id = pr.id
        if rm.media_id > 0:
            rm.isMonitored = True
            monCnt = monCnt + 1
        # use the Profile ID and the Media_ID to check the
        #       profile_media table for a entry.
        #if var['movieFile']['dateAdded'] > prof.profile_lastUpd:
        #    rm.isNewer = True

        lr = datetime.fromtimestamp(mktime(time.strptime(prof.profile_lastRun, "%b %d %Y %I:%M%p")))
        # 2018-10-03T14:39:11.9966581Z
        #lu = datetime.fromtimestamp(mktime(time.strptime(var['movieFile']['dateAdded'], "%Y-%m-%d")))
        if var['hasFile']:
            plu = var['movieFile']['dateAdded'][:10] + " " + var['movieFile']['dateAdded'][11:16]
        lu = datetime.fromtimestamp(mktime(time.strptime(plu, "%Y-%m-%d %H:%M")))
        #rm.isNewer = lu # lu[:10] + " " + lu[11:16]
        if lr < lu:
            rm.isNewer = True
            monNotSync = monNotSync + 1
        else: 
            rm.isNewer = False
            monSync = monSync + 1
        rML.movielist.append(rm)
    rML.count = cnt
    rML.monitoredCount = monCnt
    rML.syncCount = monSync
    rML.notSyncCount = monNotSync

    context = {
        'system_settings': system_settings,
        'testitem': rML,
        'system_profile': prof
    }
    template = loader.get_template("MediaFileSync/movies.html")
    return HttpResponse(template.render(context, request))

