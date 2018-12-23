from django.template import loader
from django.http import HttpResponse
from jibarr.models  import Settings, Profile, ProfileRadarr, radarrMovieList, radarrMovie
from urllib.request import urlopen
import json, time
from time import mktime
from datetime import datetime
from django.template import loader
from threading import Thread, Lock
import math

threadLock = Lock()
pageSize = 250

def index(request):
    prof_id = 1
    try:
        prof_id = request.session["prof_id"]
    except KeyError:
        pass
    system_settings = Settings.objects.all()[:1].get()
    prof_list = Profile.objects.all()
    
    rdl = get_movie_info(system_settings)
    rdml = rdl.movielist
    rdml.sort(key=lambda x: x.lastUpdt.lower(), reverse=True)
    
    radarr_list = radarrMovieList()
    radarr_list.movielist = rdml[:5]

    context = {
        'system_settings': system_settings,
        'prof_list': prof_list,
        'prof_id': prof_id,
        'radarr_list': radarr_list
    }
    template = loader.get_template("jibarr/index.html")
    return HttpResponse(template.render(context, request))

def get_movie_info(system_settings):
    
    countURL = urlopen(system_settings.radarr_path + "/api/movie?page=1&pageSize=1&apikey=" + system_settings.radarr_apikey).read()
    numberOfMovies = json.loads(countURL)['totalRecords']
    pages = math.ceil(numberOfMovies/ pageSize)
    results = radarrMovieList()
    results.movielist.clear
    results.movielist = [{} for x in range(numberOfMovies)]
    threads = []
    for nn in range(pages):     
        process = Thread(target=get_pages, args=[system_settings, nn, results])
        process.start()
        threads.append(process)

    for process in threads:
        process.join()
      
    results.count = numberOfMovies

    return results

def get_pages(system_settings, nn, results):
    global pageSize
    data = urlopen(system_settings.radarr_path + "/api/movie?page=" + str(nn+1) + "&pageSize=" + str(pageSize) + "&apikey=" + system_settings.radarr_apikey).read()
    pageAdd = nn * pageSize

    output = json.loads(data)
    #create a list of threads
    threads = []
    for ii in range(len(output["records"])):
        # We start one thread per url present.
        process = Thread(target=process_movie, args=[output["records"][ii], results.movielist, ii+pageAdd])
        process.start()
        threads.append(process)
    # We now pause execution on the main thread by 'joining' all of our started threads.
    for process in threads:
        process.join()

def process_movie (var, result, index):
    rm = radarrMovie()
    rm.title = var['title']
    rm.r_id = var['id']
    rm.titleSlug = var['titleSlug']
    try:
        rd = datetime(int(var['inCinemas'][:4]), int(var['inCinemas'][5:7]), int(var['inCinemas'][8:10])).date()
        #rd = datetime(int(var['inCinemas'][:4]), int(var['inCinemas'][5:7]), int(var['inCinemas'][8:10])
        # datetime.fromtimestamp(mktime(time.strptime(pr.lastRun, "%b %d %Y %I:%M%p")))
        rm.releaseDate = rd # var['inCinemas'][:4] + ', ' + var['inCinemas'][5:7] + ', ' + var['inCinemas'][8:10]

    except KeyError:
        pass
  
    if var['hasFile']:
        rm.folderName = var["folderName"]
        rm.fileName =  var["movieFile"]["relativePath"]
        rm.size = var["movieFile"]["size"]
        plu = var['movieFile']['dateAdded'][:10] + " " + var['movieFile']['dateAdded'][11:16]
        rm.lastUpdt = plu
        
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
    
    try:
        rm.quality = var["movieFile"]["quality"]["quality"]["name"]
    except KeyError:
        pass
    
    result[index] = rm