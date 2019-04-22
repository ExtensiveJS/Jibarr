from jibarr.models import SiteSettings, Profile, ProfileSonarr, ProfileSonarrEpisode, sonarrShow, SonarrShowMedia, sonarrShowList, SonarrEpisodeMedia, PageStuff, sonarrSeason, sonarrEpisode
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

def showdetails(request):
    prof_id = 1
    try:
        prof_id = request.session["prof_id"]
    except KeyError:
        pass
    show_id = 0
    try:
        show_id = request.GET.get("id")
    except:
        pass
    show = SonarrShowMedia()
    try:
        show = SonarrShowMedia.objects.get(sonarr_id=show_id)
    except:
        pass

    seasCount = 0
    
    #pseList = ProfileSonarrEpisode.objects.filter(profile_id=prof_id)
    psList = ProfileSonarr.objects.filter(profile_id=prof_id)
    pseList = ProfileSonarrEpisode.objects.filter(profile_id=prof_id)

    show.isMonitored = False
    for ps in psList:
        if ps.sonarr_id == show.sonarr_id:
            show.isMonitored = True

    show.seasons = [sonarrSeason()] * 0
    epC = 0
    while seasCount < show.seasonCount:
        seas = sonarrSeason()
        seas.title = 'Season ' + str(seasCount + 1)
        #seas.episodes.clear()
        seas.episodes = [SonarrEpisodeMedia()] * 0
        
        for seasEp in SonarrEpisodeMedia.objects.filter(seriesId=show.sonarr_id,seasonNumber=seasCount + 1):
            se = sonarrEpisode()
            se.id = seasEp.id
            se.sonarr_id = seasEp.sonarr_id
            se.seriesId = seasEp.seriesId
            se.episodeNumber = seasEp.episodeNumber
            se.title = seasEp.title
            se.seasonNumber = seasEp.seasonNumber
            se.path = seasEp.path
            se.dateAdded = seasEp.dateAdded
            se.quality = seasEp.quality
            se.description = seasEp.description
            se.airDate = seasEp.airDate
            se.size = seasEp.size

            se.isMonitored = show.isMonitored

            se.isNewer = False

            if show.isMonitored:
                se.isNewer = True
                for pse in pseList:
                    if pse.sonarr_id == se.sonarr_id:
                        pseLr = datetime.fromtimestamp(mktime(time.strptime(pse.lastRun, "%b %d %Y %H:%M:%S")))
                        seDa = datetime.fromtimestamp(mktime(time.strptime(se.dateAdded, "%Y-%m-%d %H:%M")))
                        if seDa < pseLr:
                            se.isNewer = False
            
            seas.episodes.append(se)
            epC += 1
        show.seasons.append(seas)
        seasCount = seasCount + 1
    

    system_settings = SiteSettings.objects.all()[:1].get()
    system_settings.newVersion = SiteSettings.checkVersion()

    isSonarrConnected = settings.isSonarrConnected
    system_settings.isSonarrConnected = isSonarrConnected

    prof_list = Profile.objects.all()
    prof = Profile.objects.get(id=prof_id)
    
    context = {
        'system_settings': system_settings,
        'system_profile': prof,
        'show': show,
        'prof_list': prof_list,
        'prof_id': prof_id
    }
    template = loader.get_template("jibarr/showdetails.html")
    return HttpResponse(template.render(context, request))