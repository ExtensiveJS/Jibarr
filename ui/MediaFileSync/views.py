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
from .models import Media, Settings, radarrMovie, radarrMovieList, Profile, ProfileMedia
from .models2 import Movies

#def syncprocessor(request):
#    #runSimulate = True
#    #strPage = "...processing started @ " + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "<br />"
#    #lastRun = "Mar 29 1971 6:07PM"
#    #strPage = MediaFileSync.checkFolder.checkFolder("d:/videos/","d:/temp/", datetime.fromtimestamp(mktime(time.strptime(lastRun, "%b %d %Y %I:%M%p"))), strPage, runSimulate)
#    #strPage += "...processing ended @ " + datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#    #return HttpResponse(strPage)
#    context = {}
#    template = loader.get_template("MediaFileSync/index.html")
#    return HttpResponse(template.render(context, request))

#def simulated(request):
#    context = {}
#    template = loader.get_template("MediaFileSync/simulated.html")
#    return HttpResponse(template.render(context, request))

#def runsimulated(request):
#    return HttpResponseRedirect("http://google.com")

def index(request):
    media_list = Media.objects.all() 
    radarr_list = Movies.objects.using("radarr").all()
    system_settings = Settings.objects.all()[:1].get()
    filtered_list = []

    for val in radarr_list:
        for val2 in media_list:
            if val.id == val2.media_id:
                filtered_list.append(val)


    context = {
        'media_list': media_list,
        'radarr_list': radarr_list,
        'filtered_list': filtered_list,
        'system_settings': system_settings
    }
    template = loader.get_template("MediaFileSync/index.html")
    return HttpResponse(template.render(context, request))

def profiles(request):
    system_settings = Settings.objects.all()[:1].get()
    context = {
        'system_settings': system_settings
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
    prof = Profile.objects.all()[:1].get()
    rML = radarrMovieList()
    rML.movielist.clear
    mList = Media.objects.all()
    data = urlopen("http://localhost:7878/api/movie?apikey=7b8c09c2a62b4cc6917be34043f67313").read()
    output = json.loads(data)
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

        # find the media_id from the Media table
        for mD in mList:
            if mD.media_source_id == var["id"]:
                rm.media_id = mD.media_id
        if rm.media_id > 0:
            rm.isMonitored = True
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
        else: 
            rm.isNewer = False
        rML.movielist.append(rm)
    rML.count = cnt

    context = {
        'system_settings': system_settings,
        'testitem': rML
    }
    template = loader.get_template("MediaFileSync/movies.html")
    return HttpResponse(template.render(context, request))

