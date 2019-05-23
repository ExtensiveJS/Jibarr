from jibarr.models import SiteSettings, Profile, ProfileSonarr, sonarrShow, SonarrShowMedia, SonarrEpisodeMedia, sonarrShowList, PageStuff
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

threadLock = Lock()

def shows(request):
    prof_id = 1
    try:
        prof_id = request.session["prof_id"]
    except KeyError:
        pass
    system_settings = SiteSettings.objects.all()[:1].get()
    system_settings.newVersion = SiteSettings.checkVersion()

    isSonarrConnected = settings.isSonarrConnected
    system_settings.isSonarrConnected = isSonarrConnected

    prof_list = Profile.objects.all()
    prof = Profile.objects.get(id=prof_id)
    

    pageNum = 1
    try:
        if(request.GET.get("page")):
            pageNum = request.GET.get("page")
    except KeyError:
        pass
    ssml = get_show_info(system_settings, prof)
    ssml.showlist.sort(key=lambda x: x.title.lower(), reverse=False)
    searchCriteria = ""
    try:
        if(request.GET.get("search")):
            searchCriteria = request.GET.get("search")
    except:
        pass
    if(searchCriteria):
        ssml.showlist = [x for x in ssml.showlist if bool(re.search(re.compile(searchCriteria, re.IGNORECASE),x.title))]

    filterCriteria = "all"
    try:
        if(request.GET.get("filter")):
            filterCriteria = request.GET.get("filter")
    except:
        pass

    if(filterCriteria=='monitored'):
        ssml.showlist = [x for x in ssml.showlist if x.isMonitored]
    
    if(filterCriteria=='unmonitored'):
        ssml.showlist = [x for x in ssml.showlist if x.isMonitored == False]

    ssml.filterCriteria = filterCriteria
    paginator = Paginator(ssml.showlist, 25)
    if(int(pageNum) > paginator.num_pages):
        pageNum = 1
    pageStuff = PageStuff
    pageStuff.pageNumber = pageNum
    pageStuff.totalPages = paginator.num_pages
    pageStuff.perPage = 5
    pageStuff.totalRecords = paginator.count

    ssml.showlist = paginator.page(int(pageNum))

    context = {
        'system_settings': system_settings,
        'system_profile': prof,
        'show_list': ssml,
        'prof_list': prof_list,
        'prof_id': prof_id
    }
    template = loader.get_template("jibarr/shows.html")
    return HttpResponse(template.render(context, request))

def get_show_info(system_settings, prof):
    sSL = sonarrShowList()
    sSL.showlist.clear

    psList = ProfileSonarr.objects.filter(profile_id=prof.id)

    cnt = 0
    epCnt = 0
    monCnt = 0
    for var in SonarrShowMedia.objects.all():
        cnt = cnt + 1
        ss = sonarrShow()
        ss.id = var.id
        ss.title = var.title
        ssDesc = (var.description[:500] + ' [...]') if len(var.description) > 500 else var.description
        ss.description = ssDesc
        ss.sonarr_id = var.sonarr_id
        ss.year = var.year
        ss.imdbId = var.imdbId
        ss.tvdbId = var.tvdbId
        ss.tvRageId = var.tvRageId
        ss.tvMazeId = var.tvMazeId
        ss.path = var.path
        ss.rating = var.rating
        ss.seasonCount = var.seasonCount
        ss.episodeCount = var.episodeCount
        ss.episodeFileCount = var.episodeFileCount
        ss.episodePercentage = round((var.episodeFileCount / var.episodeCount) * 100)
        epCnt = epCnt + var.episodeCount
        ss.isMonitored = False
        ss.isNewer = False
        ss.status = var.status

        #mId = 0
        for ps in psList:
            if ps.sonarr_id == var.sonarr_id:
                #ss.sonarr_id = ps.id
                #mId = ps.id
                #psLr = datetime.fromtimestamp(mktime(time.strptime(ps.lastRun, "%b %d %Y %I:%M%p")))
                ss.isMonitored = True
                monCnt = monCnt + 1
        
        #if ss.id > 0:
        #    ss.isMonitored = True    
        #    with threadLock:
                

        sSL.showlist.append(ss)
    sSL.count = cnt
    sSL.episodeCount = epCnt
    sSL.monitoredCount = monCnt
    return sSL