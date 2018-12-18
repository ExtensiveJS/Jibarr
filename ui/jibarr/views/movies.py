from jibarr.models import Settings, radarrMovie, radarrMovieList, Profile, ProfileRadarr
from urllib.request import urlopen
import json
from time import mktime
from datetime import datetime
import time
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from threading import Thread, Lock
import math

threadLock = Lock()
pageSize = 250


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
    prof_list = Profile.objects.all()
    prof = Profile.objects.get(id=prof_id)
    
    cnt = 0
    monCnt = 0
    monSync = 0
    monNotSync = 0

    rdml = get_movie_info(system_settings, prof)
    rdml.movielist = [x for x in rdml.movielist if x.quality]
    rdml.movielist.sort(key=lambda x: x.title.lower(), reverse=False)

    context = {
        'system_settings': system_settings,
        'testitem': rdml,
        'system_profile': prof,
        'prof_list': prof_list,
        'prof_id': prof_id
    }
    template = loader.get_template("jibarr/movies.html")
    return HttpResponse(template.render(context, request))
  

def get_movie_info(system_settings, prof):
    prList = ProfileRadarr.objects.filter(profile_id=prof.id)

    countURL = urlopen(system_settings.radarr_path + "/api/movie?page=1&pageSize=1&apikey=" + system_settings.radarr_apikey).read()
    numberOfMovies = json.loads(countURL)['totalRecords']
    pages = math.ceil(numberOfMovies/ pageSize)
    results = radarrMovieList()
    results.movielist.clear
    results.movielist = [{} for x in range(numberOfMovies)]
    threads = []
    for nn in range(pages):     
        process = Thread(target=get_pages, args=[system_settings, nn, prList, prof, results])
        process.start()
        threads.append(process)

    for process in threads:
        process.join()
      
    results.count = numberOfMovies
    results.monitoredCount = monCnt
    results.syncCount = monSync
    results.notSyncCount = monNotSync

    return results

def get_pages(system_settings, nn, prList, prof, results):
    global pageSize
    data = urlopen(system_settings.radarr_path + "/api/movie?page=" + str(nn+1) + "&pageSize=" + str(pageSize) + "&apikey=" + system_settings.radarr_apikey).read()
    pageAdd = nn * pageSize

    output = json.loads(data)
    #create a list of threads
    threads = []
    for ii in range(len(output["records"])):
        # We start one thread per url present.
        process = Thread(target=process_movie, args=[output["records"][ii], prList, prof,  results.movielist, ii+pageAdd])
        process.start()
        threads.append(process)
    # We now pause execution on the main thread by 'joining' all of our started threads.
    for process in threads:
        process.join()

def process_movie (var, prList, prof, result, index):
    global monCnt
    global monSync
    global monNotSync

    rm = radarrMovie()
    rm.title = var['title']
    rm.r_id = var['id']
    rm.titleSlug = var['titleSlug']
    try:
        rd = var['inCinemas'][:10] # + " " + var['inCinemas'][11:16]
        rm.releaseDate = rd
        rm.releaseYear = var['inCinemas'][:4]
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
    
    try:
        rm.youtube = var["youTubeTrailerId"]
    except KeyError:
        pass
    
    try:
        rm.website = var["website"]
    except KeyError:
        pass
    
    rm.quality = ""
    try:
        rm.quality = var["movieFile"]["quality"]["quality"]["name"]
    except KeyError:
        pass

    result[index] = rm