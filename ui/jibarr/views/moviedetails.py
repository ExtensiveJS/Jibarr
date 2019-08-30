from jibarr.models import SiteSettings, Profile, ProfileRadarr, RadarrMedia, PageStuff
from urllib.request import urlopen
import json, re
from time import mktime
from datetime import datetime
import time
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.core.paginator import Paginator
from threading import Thread, Lock
from django.conf import settings

def moviedetails(request):
    prof_id = 1
    try:
        prof_id = request.session["prof_id"]
    except KeyError:
        pass
    movie_id = 0
    try:
        movie_id = request.GET.get("id")
    except:
        pass
    movie = RadarrMedia()
    try:
        movie = RadarrMedia.objects.get(radarr_id=movie_id)
        movie.year = movie.release_date[0:4]
    except:
        pass

    
    #psList = ProfileSonarr.objects.filter(profile_id=prof_id)
    #pseList = ProfileSonarrEpisode.objects.filter(profile_id=prof_id) 
    rmList = ProfileRadarr.objects.filter(profile_id=prof_id)
    movie.isMonitored = False
    for rm in rmList:
        if rm.radarr_id == movie.radarr_id:
            movie.isMonitored = True   

    system_settings = SiteSettings.objects.all()[:1].get()
    system_settings.newVersion = SiteSettings.checkVersion()

    isRadarrConnected = settings.isRadarrConnected
    system_settings.isRadarrConnected = isRadarrConnected

    prof_list = Profile.objects.all()
    prof = Profile.objects.get(id=prof_id)
    
    context = {
        'system_settings': system_settings,
        'system_profile': prof,
        'movie': movie,
        'prof_list': prof_list,
        'prof_id': prof_id
    }
    template = loader.get_template("jibarr/moviedetails.html")
    return HttpResponse(template.render(context, request))