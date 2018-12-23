from django.template import loader
from django.http import HttpResponse
from jibarr.models  import Settings, Profile, ProfileRadarr, radarrMovieList, radarrMovie, RadarrMedia
import time, math
from time import mktime
from datetime import datetime
from django.template import loader

def index(request):
    prof_id = 1
    try:
        prof_id = request.session["prof_id"]
    except KeyError:
        pass
    system_settings = Settings.objects.all()[:1].get()
    prof_list = Profile.objects.all()
    
    rdl = get_movie_info(system_settings)
    rdml = rdl.movielist
    rdml.sort(key=lambda x: x.lastUpdt.lower(), reverse=True)
    
    radarr_list = radarrMovieList()
    radarr_list.movielist = rdml[:5]

    context = {
        'system_settings': system_settings,
        'prof_list': prof_list,
        'prof_id': prof_id,
        'radarr_list': radarr_list
    }
    template = loader.get_template("jibarr/index.html")
    return HttpResponse(template.render(context, request))

def get_movie_info(system_settings):
    
    results = radarrMovieList()
    results.movielist.clear
    
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
        
        results.movielist.append(rm)

    return results