from MediaFileSync.models import Settings, radarrMovie, radarrMovieList, Profile, ProfileRadarr
from urllib.request import urlopen
import json
from time import mktime
from datetime import datetime
import time
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from threading import Thread, Lock

threadLock = Lock()

def movies(request):
    global cnt
    global monCnt
    global monSync
    global monNotSync
    prof_id = 1
    try:
        prof_id = request.session["prof_id"]
    except KeyError:
        #prof_id = 1
        pass
    system_settings = Settings.objects.all()[:1].get()
    prof_list = Profile.objects.all()
    prof = Profile.objects.get(id=prof_id)
    
    cnt = 0
    monCnt = 0
    monSync = 0
    monNotSync = 0


    context = {
        'system_settings': system_settings,
        'testitem': get_movie_info(system_settings, prof),
        'system_profile': prof,
        'prof_list': prof_list,
        'prof_id': prof_id
    }
    template = loader.get_template("MediaFileSync/movies.html")
    return HttpResponse(template.render(context, request))
  

def get_movie_info(system_settings, prof):
    prList = ProfileRadarr.objects.filter(profile_id=prof.id)
    data = urlopen(system_settings.radarr_path + "/api/movie?apikey=" + system_settings.radarr_apikey).read()
    output = json.loads(data)
    results = radarrMovieList()
    results.movielist.clear
    results.movielist = [{} for x in output]

    #create a list of threads
    threads = []
    # In this case 'urls' is a list of urls to be crawled.
    for ii in range(len(output)):
        # We start one thread per url present.
        process = Thread(target=process_movie, args=[output[ii], prList, prof,  results.movielist, ii])
        process.start()
        threads.append(process)
    # We now pause execution on the main thread by 'joining' all of our started threads.
    # This ensures that each has finished processing the urls.
    for process in threads:
        process.join()
    # At this point, results for each URL are now neatly stored in order in 'results'
      
    results.count = cnt
    results.monitoredCount = monCnt
    results.syncCount = monSync
    results.notSyncCount = monNotSync

    return results

def process_movie (var, prList, prof, result, index):
    global cnt
    global monCnt
    global monSync
    global monNotSync
    with threadLock:
        cnt = cnt + 1
    rm = radarrMovie()
    rm.title = var['title']
    rm.r_id = var['id']
    try:
        rd = var['inCinemas'][:10] # + " " + var['inCinemas'][11:16]
        rm.releaseDate = rd
    except KeyError:
        pass
  
    mId = 0
    for pr in prList:
        if pr.radarr_id == var["id"]:
            rm.media_id = pr.id
            mId = pr.id
            prLr = datetime.fromtimestamp(mktime(time.strptime(pr.lastRun, "%b %d %Y %I:%M%p")))
    
    if rm.media_id > 0:
        rm.isMonitored = True    
        with threadLock:
            monCnt = monCnt + 1

    if var['hasFile']:
        rm.folderName = var["folderName"]
        rm.fileName =  var["movieFile"]["relativePath"]
        rm.size = var["movieFile"]["size"]
        plu = var['movieFile']['dateAdded'][:10] + " " + var['movieFile']['dateAdded'][11:16]
        rm.lastUpdt = plu
        lu = datetime.fromtimestamp(mktime(time.strptime(plu, "%Y-%m-%d %H:%M")))
        if mId > 0:
            if lu >  prLr:
                rm.isNewer = True
                with threadLock:
                    monNotSync = monNotSync + 1
            else:
                rm.isNewer = False
                with threadLock:
                    monSync = monSync + 1
        else:
            rm.isNewer = False      

    rm.rating = var["ratings"]["value"]

    try:
        rm.tmdbid = var["tmdbId"]
    except KeyError:
        pass
    
    try:
        rm.imdbid = var["imdbId"]
    except KeyError:
        pass
    
    result[index] = rm