from django.template import loader
from django.http import HttpResponse
from jibarr.models import SiteSettings, Profile, ProfileSonarr, ProfileSonarrEpisode, sonarrShowList, sonarrShow, sonarrEpisode, sonarrEpisodeList, SonarrShowMedia, SonarrEpisodeMedia, SonarrSeasonExclusions
from urllib.request import urlopen
import json, time, math
from time import mktime
from datetime import datetime

def runsyncshows(request):
    prof_id = 1
    try:
        prof_id = request.session["prof_id"]
    except KeyError:
        #prof_id = 1
        pass
    system_settings = SiteSettings.objects.all()[:1].get()
    system_settings.newVersion = SiteSettings.checkVersion()
    prof_list = Profile.objects.all()
    
    sonarr_episode_list = sonarrEpisodeList()
    profile_sonarr_show_list = ProfileSonarr.objects.filter(profile_id=prof_id)
    totalFileSize = 0

    for pss in profile_sonarr_show_list:
        sel = SonarrEpisodeMedia.objects.filter(seriesId=pss.sonarr_id)
        for se in sel:
            # check if the season is excluded
            if SonarrSeasonExclusions.objects.filter(series_id=pss.sonarr_id,seasonNumber=se.seasonNumber,profile_id=prof_id).count() < 1:
                # check if the episode is monitored
                if ProfileSonarrEpisode.objects.filter(profile_id=prof_id,sonarr_id=se.sonarr_id).count() == 1:
                    pse = ProfileSonarrEpisode.objects.get(profile_id=prof_id,sonarr_id=se.sonarr_id)
                    if pse:
                        pseLr = datetime.fromtimestamp(mktime(time.strptime(pse.lastRun, "%b %d %Y %H:%M:%S")))
                        selu = datetime.fromtimestamp(mktime(time.strptime(se.dateAdded, "%Y-%m-%d %H:%M")))
                        if selu > pseLr:
                            sem = SonarrEpisodeMedia.objects.get(sonarr_id=se.sonarr_id)
                            ss = SonarrShowMedia.objects.get(sonarr_id=sem.seriesId)
                            sem.showName = ss.title
                            sem.fileSize = convert_size(sem.size)
                            sonarr_episode_list.episodelist.append(sem)
                            totalFileSize = totalFileSize + sem.size
                else:
                    # not in PSE, add it to sync list
                    sem = SonarrEpisodeMedia.objects.get(sonarr_id=se.sonarr_id)
                    ss = SonarrShowMedia.objects.get(sonarr_id=sem.seriesId)
                    sem.showName = ss.title
                    sem.fileSize = convert_size(sem.size)
                    sonarr_episode_list.episodelist.append(sem)
                    totalFileSize = totalFileSize + sem.size


    sonarr_episode_list.episodelist.sort(key=lambda x: x.showName.lower(), reverse=False)    
    sonarr_episode_list.totalSize = convert_size(totalFileSize)

    context = {
        'system_settings': system_settings,
        'prof_list': prof_list,
        'prof_id': prof_id,
        'sonarr_episode_list': sonarr_episode_list,
        'prof_lastPath': Profile.objects.get(id=prof_id).profile_lastPath
    }
    template = loader.get_template("jibarr/runsyncshows.html")
    return HttpResponse(template.render(context, request))


def convert_size(size_bytes):
   if size_bytes == 0:
       return "0B"
   size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
   i = int(math.floor(math.log(size_bytes, 1024)))
   p = math.pow(1024, i)
   s = round(size_bytes / p, 2)
   return "%s %s" % (s, size_name[i])