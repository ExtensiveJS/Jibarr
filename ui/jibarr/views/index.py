from django.template import loader
from django.http import HttpResponse
from jibarr.models  import SiteSettings, Profile, ProfileRadarr, radarrMovieList, radarrMovie, RadarrMedia
import time, math
from time import mktime
from datetime import datetime
from django.template import loader
from urllib.request import urlopen
import json

def index(request):
    prof_id = 1
    try:
        prof_id = request.session["prof_id"]
    except KeyError:
        pass
    system_settings = SiteSettings.objects.all()[:1].get()
    system_settings.newVersion = SiteSettings.checkVersion()
    prof_list = Profile.objects.all()
    
    rdl = get_movie_info(system_settings,prof_id)
    rdml = rdl.movielist
    rdml.sort(key=lambda x: x.lastUpdt.lower(), reverse=True)
    
    radarr_list = radarrMovieList()
    radarr_list.movielist = rdml[:10]

    isConnected = False
    try:
        data = urlopen(system_settings.radarr_path + "/api/system/status/?apikey=" + system_settings.radarr_apikey).read()
        output = json.loads(data)
        isConnected = True
    except:
        pass

    system_settings.isConnected = isConnected

    context = {
        'system_settings': system_settings,
        'prof_list': prof_list,
        'prof_id': prof_id,
        'radarr_list': radarr_list
    }
    template = loader.get_template("jibarr/index.html")
    return HttpResponse(template.render(context, request))

def get_movie_info(system_settings,prof_id):
    
    results = radarrMovieList()
    results.movielist.clear
    
    prList = ProfileRadarr.objects.filter(profile_id=prof_id)

    for var in RadarrMedia.objects.all():

        rm = radarrMovie()
        rm.title = var.title
        rm.r_id = var.radarr_id
        rm.titleSlug = var.title_slug
        rm.releaseDate = var.release_date
        rm.folderName = var.folder_name
        rm.fileName =  var.file_name
        rm.size = var.size
        rm.lastUpdt = var.last_updt
        rm.rating = var.rating
        rm.tmdbid = var.tmdbid
        rm.imdbid = var.imdbid
        rm.youtube = var.youtube
        rm.website = var.website
        rm.quality = var.quality
        
        for pr in prList:
            if pr.radarr_id == var.radarr_id:
                rm.media_id = pr.id
                rm.isMonitored = True

        results.movielist.append(rm)

    return results