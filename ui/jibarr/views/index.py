from django.template import loader
from django.http import HttpResponse
from jibarr.models  import sonarrEpisodeList, sonarrEpisode, SonarrEpisodeMedia, sonarrShowList, SonarrShowMedia, sonarrShow, ProfileSonarr, SiteSettings, Profile, ProfileRadarr, radarrMovieList, radarrMovie, RadarrMedia
import time, math
from time import mktime
from datetime import datetime
from django.template import loader
from urllib.request import urlopen
from django.conf import settings
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
    radarr_list.movielist = rdml[:5]

    #sl = get_show_info(system_settings,prof_id)
    #ssl = sl.showlist
    #ssl.sort(key=lambda x:x.lastInfoSync, reverse=True)
    sonarr_list = sonarrShowList()
    #sonarr_list.showlist = ssl[:5]

    sel = get_episode_info(system_settings,prof_id)
    sell = sel.episodelist
    sell.sort(key=lambda x:x.dateAdded, reverse=True)

    for var in sell:
        ss = SonarrShowMedia.objects.get(sonarr_id=var.seriesId)
        ss.episodePercentage = round((ss.episodeFileCount / ss.episodeCount) * 100)
        ss.isMonitored = False
        try:
            ProfileSonarr.objects.get(sonarr_id=var.seriesId)
            ss.isMonitored = True
        except:
            pass
        ss.isNewer = True
        sonarr_list.showlist.append(ss)
    
    sonarr_list2 = sonarrShowList()
    for var in sonarr_list.showlist:
        found = False
        for var2 in sonarr_list2.showlist:
            if var.sonarr_id == var2.sonarr_id:
                found = True
        if found == False:
            sonarr_list2.showlist.append(var)
            if len(sonarr_list2.showlist) >= 5:
                break



    isConnected = settings.isConnected
    isSonarrConnected = settings.isSonarrConnected

    system_settings.isConnected = isConnected
    system_settings.isSonarrConnected = isSonarrConnected
    
    context = {
        'system_settings': system_settings,
        'prof_list': prof_list,
        'prof_id': prof_id,
        'radarr_list': radarr_list,
        'sonarr_list': sonarr_list2
    }
    template = loader.get_template("jibarr/index.html")
    return HttpResponse(template.render(context, request))

def get_show_info(system_settings,prof_id):
    
    results = sonarrShowList()
    results.showlist.clear
    
    psList = ProfileSonarr.objects.filter(profile_id=prof_id)

    for var in SonarrShowMedia.objects.all():

        ss = sonarrShow()
        ss.title = var.title
        ss.s_id = var.sonarr_id
        ss.sonarr_id = var.sonarr_id
        ss.lastInfoSync = var.lastInfoSync
        ss.title_slug = var.title_slug
        ss.year = var.year
        ss.path = var.path
        ss.rating = var.rating
        ss.tvdbId = var.tvdbId
        ss.tvRageId = var.tvRageId
        ss.tvMazeId = var.tvMazeId
        ss.imdbId = var.imdbId
        ss.seasonCount = var.seasonCount
        ss.episodeCount = var.episodeCount
        ss.episodeFileCount = var.episodeFileCount
        ss.description = var.description
        ss.episodePercentage = round((var.episodeFileCount / var.episodeCount) * 100)
        
        for ps in psList:
            if ps.sonarr_id == var.sonarr_id:
                #rm.media_id = pr.id
                ss.isMonitored = True

        results.showlist.append(ss)

    return results

def get_episode_info(system_settings,prof_id):
    
    results = sonarrEpisodeList()
    results.episodelist.clear
    
    psList = ProfileSonarr.objects.filter(profile_id=prof_id)

    for ep in SonarrEpisodeMedia.objects.all():
        se = sonarrEpisode()
        se.airDate = ep.airDate
        se.dateAdded = ep.dateAdded
        se.description = ep.description
        se.episodeNumber = ep.episodeNumber
        se.id = ep.id
        se.path = ep.path
        se.quality = ep.quality
        se.seasonNumber = ep.seasonNumber
        se.seriesId = ep.seriesId
        se.size = ep.size
        se.sonarr_id = ep.sonarr_id
        se.title = ep.title
        se.isNewer = True
        for ps in psList:
            if ps.sonarr_id == se.seriesId:
                se.isMonitored = True
        results.episodelist.append(se)

    return results

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