from jibarr.models import Settings, radarrMovie, radarrMovieList, Profile, ProfileRadarr, PageStuff, RadarrMedia
from time import mktime
from datetime import datetime
import time
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.core.paginator import Paginator
import math
from urllib.request import urlopen
import json

def movies(request):
    global cnt
    global monCnt
    global monSync
    global monNotSync
    prof_id = 1
    try:
        prof_id = request.session["prof_id"]
    except KeyError:
        pass
    system_settings = Settings.objects.all()[:1].get()

    isConnected = False
    try:
        data = urlopen(system_settings.radarr_path + "/api/system/status/?apikey=" + system_settings.radarr_apikey).read()
        json.loads(data)
        isConnected = True
    except:
        pass

    system_settings.isConnected = isConnected

    prof_list = Profile.objects.all()
    prof = Profile.objects.get(id=prof_id)
    
    cnt = 0
    monCnt = 0
    monSync = 0
    monNotSync = 0

    pageNum = 1
    try:
        if(request.GET.get("page")):
            pageNum = request.GET.get("page")
    except KeyError:
        pass
    rdml = get_movie_info(system_settings, prof)
    rdml.movielist = [x for x in rdml.movielist if x.quality]
    rdml.movielist.sort(key=lambda x: x.title.lower(), reverse=False)

    filterCriteria = "all"
    try:
        if(request.GET.get("filter")):
            filterCriteria = request.GET.get("filter")
    except KeyError:
        pass

    if(filterCriteria=='monitored'):
        rdml.movielist = [x for x in rdml.movielist if x.isMonitored]
    
    if(filterCriteria=='unmonitored'):
        rdml.movielist = [x for x in rdml.movielist if x.isMonitored == False]
    
    rdml.filterCriteria = filterCriteria
    paginator = Paginator(rdml.movielist, 25)
    if(int(pageNum) > paginator.num_pages):
        pageNum = 1
    pageStuff = PageStuff
    pageStuff.pageNumber = pageNum
    pageStuff.totalPages = paginator.num_pages
    pageStuff.perPage = 5
    pageStuff.totalRecords = paginator.count

    
    rdml.movielist = paginator.page(int(pageNum))

    context = {
        'system_settings': system_settings,
        'testitem': rdml,
        'system_profile': prof,
        'prof_list': prof_list,
        'prof_id': prof_id,
        'pageStuff': pageStuff
    }
    template = loader.get_template("jibarr/movies.html")
    return HttpResponse(template.render(context, request))
  

def get_movie_info(system_settings, prof):
    global monCnt
    global monSync
    global monNotSync

    results = radarrMovieList()
    results.movielist.clear
    
    prList = ProfileRadarr.objects.filter(profile_id=prof.id)

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
        
        mId = 0
        for pr in prList:
            if pr.radarr_id == var.radarr_id:
                rm.media_id = pr.id
                mId = pr.id
                prLr = datetime.fromtimestamp(mktime(time.strptime(pr.lastRun, "%b %d %Y %H:%M:%S")))
        
        if rm.media_id > 0:
            rm.isMonitored = True    
            monCnt = monCnt + 1

        if mId > 0:
            lu = datetime.fromtimestamp(mktime(time.strptime(var.last_updt, "%Y-%m-%d %H:%M")))
            if lu >  prLr:
                rm.isNewer = True
                monNotSync = monNotSync + 1
            else:
                rm.isNewer = False
                monSync = monSync + 1
        else:
            rm.isNewer = False

        results.movielist.append(rm)

    results.monitoredCount = monCnt
    results.syncCount = monSync
    results.notSyncCount = monNotSync
    
    return results