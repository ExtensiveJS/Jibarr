from django.template import loader
from django.http import HttpResponse
from MediaFileSync.models  import Settings, Profile, ProfileRadarr, radarrMovieList, radarrMovie
from urllib.request import urlopen
import json

def index(request):
    #http://localhost:7878/api/movie/1?apikey=7b8c09c2a62b4cc6917be34043f67313
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
    
        data = urlopen(system_settings.radarr_path + "/api/movie/" + str(rid) + "?apikey=" + system_settings.radarr_apikey).read()
        output = json.loads(data)  

        rm = radarrMovie()
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
        radarr_list.movielist.append(rm)
        #for key, value in data.iteritems():
        #for key in output.items():
            #rm = radarrMovie()
            #rm.title = var['title']
            #rm.r_id = key['id']
            #try:
            #    rm.releaseDate = key['inCinemas'][:10]
            #except KeyError:
            #    pass
            #radarr_list.movielist.append(rm)



    context = {
        'system_settings': system_settings,
        'prof_list': prof_list,
        'prof_id': prof_id,
        'radarr_list': radarr_list
    }
    template = loader.get_template("MediaFileSync/index.html")
    return HttpResponse(template.render(context, request))