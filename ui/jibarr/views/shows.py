from jibarr.models import SiteSettings, Profile, ProfileSonarr, sonarrShow, sonarrShowList
from urllib.request import urlopen
import json
from time import mktime
from datetime import datetime
import time
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from threading import Thread, Lock

threadLock = Lock()

def shows(request):
    prof_id = 1
    try:
        prof_id = request.session["prof_id"]
    except KeyError:
        pass
    system_settings = SiteSettings.objects.all()[:1].get()
    system_settings.newVersion = SiteSettings.checkVersion()
    prof_list = Profile.objects.all()
    prof = Profile.objects.get(id=prof_id)
    
    context = {
        'system_settings': system_settings,
        'system_profile': prof,
        'show_list': get_show_info(system_settings, prof),
        'prof_list': prof_list,
        'prof_id': prof_id
    }
    template = loader.get_template("jibarr/shows.html")
    return HttpResponse(template.render(context, request))

def get_show_info(system_settings, prof):
    sSL = sonarrShowList()
    sSL.showlist.clear
    psList = ProfileSonarr.objects.filter(profile_id=prof.id)
    data = urlopen(system_settings.sonarr_path + "/api/series?apikey=" + system_settings.sonarr_apikey).read()
    output = json.loads(data)
    cnt = 0
    epCnt = 0
    monCnt = 0
    for var in output:
        cnt = cnt + 1
        ss = sonarrShow()
        ss.title = var['title']
        ss.s_id = var['id']
        ss.year = var['year']
        try:
            ss.imdbId = var["imdbId"]
        except KeyError:
            pass
        ss.tvdbId = var['tvdbId']
        ss.tvRageId = var['tvRageId']
        try:
            ss.status = var["staus"]
        except KeyError:
            pass
        ss.folderName = var['path']
        ss.rating = var['ratings']['value']
        ss.seasonCount = var['seasonCount']
        ss.episodeCount = var['episodeCount']
        epCnt = epCnt + var['episodeCount']
        ss.isMonitored = False
        ss.isNewer = False

        mId = 0
        for ps in psList:
            if ps.sonarr_id == var["id"]:
                ss.media_id = ps.id
                mId = ps.id
                psLr = datetime.fromtimestamp(mktime(time.strptime(ps.lastRun, "%b %d %Y %I:%M%p")))
        
        if ss.media_id > 0:
            ss.isMonitored = True    
            with threadLock:
                monCnt = monCnt + 1

        if var['episodeCount'] > 0:
            ss.isNewer = True

        sSL.showlist.append(ss)
    sSL.count = cnt
    sSL.episodeCount = epCnt
    sSL.monitoredCount = monCnt
    return sSL