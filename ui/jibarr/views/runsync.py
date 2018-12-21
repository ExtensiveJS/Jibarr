from django.template import loader
from django.http import HttpResponse
from jibarr.models import Settings, Profile, ProfileRadarr, radarrMovieList, radarrMovie
from urllib.request import urlopen
import json, time, math
from time import mktime
from datetime import datetime

def runsync(request):
    prof_id = 1
    try:
        prof_id = request.session["prof_id"]
    except KeyError:
        #prof_id = 1
        pass
    system_settings = Settings.objects.all()[:1].get()
    prof_list = Profile.objects.all()
    radarr_list = radarrMovieList()
    
    profile_radarr_list = ProfileRadarr.objects.filter(profile_id=prof_id)
    for pr in profile_radarr_list:
        rid = pr.radarr_id
        prLr = datetime.fromtimestamp(mktime(time.strptime(pr.lastRun, "%b %d %Y %H:%M:%S")))
        # %b %d %Y %H:%M:%S
        data = urlopen(system_settings.radarr_path + "/api/movie/" + str(rid) + "?apikey=" + system_settings.radarr_apikey).read()
        output = json.loads(data)  

        rm = radarrMovie()
        rm.prid = pr.id
        rm.id = output['id']
        rm.title = output['title']
        try:
            rm.releaseDate = output['inCinemas'][:4]
        except KeyError:
            pass

        try:
            rm.tmdbid = output["tmdbId"]
        except KeyError:
            pass
        
        if output['hasFile']:
            plu = output['movieFile']['dateAdded'][:10] + " " + output['movieFile']['dateAdded'][11:16]
            #rm.lastUpdt = plu
            rmlu = datetime.fromtimestamp(mktime(time.strptime(plu, "%Y-%m-%d %H:%M")))
            rm.fileSize = convert_size(output['sizeOnDisk'])
            
        if rmlu > prLr:
            radarr_list.movielist.append(rm)

    context = {
        'system_settings': system_settings,
        'prof_list': prof_list,
        'prof_id': prof_id,
        'radarr_list': radarr_list,''
        'prof_lastPath': Profile.objects.get(id=prof_id).profile_lastPath
    }
    template = loader.get_template("jibarr/runsync.html")
    return HttpResponse(template.render(context, request))

def convert_size(size_bytes):
   if size_bytes == 0:
       return "0B"
   size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
   i = int(math.floor(math.log(size_bytes, 1024)))
   p = math.pow(1024, i)
   s = round(size_bytes / p, 2)
   return "%s %s" % (s, size_name[i])