import os, shutil, json, time
from jibarr.models import Settings, radarrMovie, Logs, RadarrMedia
from urllib.request import urlopen
from celery import task
from datetime import datetime


@task
def RadarrSync(forceload):
    try:
        Logs.objects.create(log_type='Sync',log_category='System',log_message='Radarr Database sync started',log_datetime=datetime.now().strftime("%b %d %Y %H:%M:%S"))
    except KeyError:
        pass
    isSuccessful = False
    system_settings = Settings.objects.all()[:1].get()

    # call to RADARR and read JSON
    data = urlopen(system_settings.radarr_path + "/api/movie?apikey=" + system_settings.radarr_apikey).read()
    output = json.loads(data)

    if forceload:
        # PURGE THE DATABASE
        RadarrMedia.objects.all().delete()

    # iterate JSON 
    for var in output:
        try:
            if forceload:
                # do an INSERT on every record
                rm = RadarrMedia
                rm.radarr_id = var['id']
                rm.title = var['title']
                rm.title_slug = var['titleSlug']
                try:
                    rm.release_date = var['inCinemas'][:10]
                except:
                    rm.release_date = ""

                if var['hasFile']:    
                    rm.folder_name = var["folderName"]
                    rm.size = var["movieFile"]["size"]
                    rm.file_name = var["movieFile"]["relativePath"]
                    rm.last_updt = var['movieFile']['dateAdded'][:10] + " " + var['movieFile']['dateAdded'][11:16]
                rm.rating = rm.rating = var["ratings"]["value"]
                try:
                    rm.tmdbid = var["tmdbId"]
                except:
                    rm.tmdbid = ""
                    pass
                
                try:
                    rm.imdbid = var["imdbId"]
                except:
                    rm.imdbid = ""
                    pass
                
                try:
                    rm.youtube = var["youTubeTrailerId"]
                except:
                    rm.youtube = ""
                    pass
                
                try:
                    rm.website = var["website"]
                except:
                    rm.website = ""
                    pass
                
                try:
                    rm.quality = var["movieFile"]["quality"]["quality"]["name"]
                except:
                    rm.quality = ""
                    pass
                
                RadarrMedia.objects.create(radarr_id = rm.radarr_id,title = rm.title,title_slug = rm.title_slug,release_date = rm.release_date,folder_name = rm.folder_name,size = rm.size,file_name = rm.file_name,last_updt = rm.last_updt,rating = rm.rating,tmdbid = rm.tmdbid,imdbid = rm.imdbid,youtube = rm.youtube,website = rm.website,quality = rm.quality)
                #rm.save()
                isSuccessful = True

            else:
                # check ID against DB
                try:
                    rm = RadarrMedia.objects.get(radarr_id=var['id'])
                except:
                    rm.id = False
                    pass

                wasUpdated = False
                ## if exist - Update
                if rm.id:
                    if rm.radarr_id != var['id']:
                        wasUpdated = True
                        rm.radarr_id = var['id']
                    if rm.title != var['title']:
                        wasUpdated = True
                        rm.title = var['title']
                    if rm.title_slug != var['titleSlug']:
                        wasUpdated = True
                        rm.title_slug = var['titleSlug']
                    try:
                        if rm.release_date != var['inCinemas'][:10]:
                            wasUpdated = True
                            rm.release_date = var['inCinemas'][:10]
                    except:
                        rm.release_date = ""

                    if var['hasFile']:    
                        if rm.folder_name != var['folderName']:
                            wasUpdated = True
                            rm.folder_name = var["folderName"]
                        if rm.size != var["movieFile"]["size"]:
                            wasUpdated = True
                            rm.size = var["movieFile"]["size"]
                        if rm.file_name != var["movieFile"]["relativePath"]:
                            wasUpdated = True
                            rm.file_name = var["movieFile"]["relativePath"]
                        if rm.last_updt != var['movieFile']['dateAdded'][:10] + " " + var['movieFile']['dateAdded'][11:16]:
                            wasUpdated = True
                            rm.last_updt = var['movieFile']['dateAdded'][:10] + " " + var['movieFile']['dateAdded'][11:16]
                    if str(rm.rating) != str(var["ratings"]["value"]):
                        wasUpdated = True
                        rm.rating = str(var["ratings"]["value"])
                    try:
                        if str(rm.tmdbid) != str(var['tmdbId']):
                            wasUpdated = True
                            rm.tmdbid = str(var["tmdbId"])
                    except:
                        rm.tmdbid = ""
                        pass
                    
                    try:
                        if rm.imdbid != var['imdbId']:
                            wasUpdated = True
                            rm.imdbid = var["imdbId"]
                    except:
                        rm.imdbid = ""
                        pass
                    
                    try:
                        if rm.youtube != var['youTubeTrailerId']:
                            wasUpdated = True
                            rm.youtube = var["youTubeTrailerId"]
                    except:
                        rm.youtube = ""
                        pass
                    
                    try:
                        if rm.website != var['website']:
                            wasUpdated = True
                            rm.website = var["website"]
                    except:
                        rm.website = ""
                        pass
                    
                    try:
                        if rm.quality != var["movieFile"]["quality"]["quality"]["name"]:
                            wasUpdated = True
                            rm.quality = var["movieFile"]["quality"]["quality"]["name"]
                    except:
                        rm.quality = ""
                        pass
                    
                    #RadarrMedia.objects.create(radarr_id = rm.radarr_id,title = rm.title,title_slug = rm.title_slug,release_date = rm.release_date,folder_name = rm.folder_name,size = rm.size,file_name = rm.file_name,last_updt = rm.last_updt,rating = rm.rating,tmdbid = rm.tmdbid,imdbid = rm.imdbid,youtube = rm.youtube,website = rm.website,quality = rm.quality)
                    if wasUpdated:
                        try:
                            Logs.objects.create(log_type='Sync',log_category='System',log_message='Updated ' + rm.title + ' from Radarr.',log_datetime=datetime.now().strftime("%b %d %Y %H:%M:%S"))
                        except:
                            pass
                        rm.save()
                    isSuccessful = True
                else:
                    ## if not exist - Insert
                    rm = RadarrMedia
                    rm.radarr_id = var['id']
                    rm.title = var['title']
                    rm.title_slug = var['titleSlug']
                    try:
                        rm.release_date = var['inCinemas'][:10] # + " " + var['inCinemas'][11:16]
                    except:
                        rm.release_date = ""

                    if var['hasFile']:    
                        rm.folder_name = var["folderName"]
                        rm.size = var["movieFile"]["size"]
                        rm.file_name = var["movieFile"]["relativePath"]
                        rm.last_updt = var['movieFile']['dateAdded'][:10] + " " + var['movieFile']['dateAdded'][11:16]
                    rm.rating = rm.rating = var["ratings"]["value"]
                    try:
                        rm.tmdbid = var["tmdbId"]
                    except:
                        rm.tmdbid = ""
                        pass
                    
                    try:
                        rm.imdbid = var["imdbId"]
                    except:
                        rm.imdbid = ""
                        pass
                    
                    try:
                        rm.youtube = var["youTubeTrailerId"]
                    except:
                        rm.youtube = ""
                        pass
                    
                    try:
                        rm.website = var["website"]
                    except:
                        rm.website = ""
                        pass
                    
                    try:
                        rm.quality = var["movieFile"]["quality"]["quality"]["name"]
                    except:
                        rm.quality = ""
                        pass
                    
                    RadarrMedia.objects.create(radarr_id = rm.radarr_id,title = rm.title,title_slug = rm.title_slug,release_date = rm.release_date,folder_name = rm.folder_name,size = rm.size,file_name = rm.file_name,last_updt = rm.last_updt,rating = rm.rating,tmdbid = rm.tmdbid,imdbid = rm.imdbid,youtube = rm.youtube,website = rm.website,quality = rm.quality)
                    try:
                        Logs.objects.create(log_type='Sync',log_category='System',log_message='Added ' + rm.title + ' from Radarr',log_datetime=datetime.now().strftime("%b %d %Y %H:%M:%S"))
                    except:
                        pass
                    isSuccessful = True
        except:
            pass

    if isSuccessful:
        ############################################### update settings last sync date
        sett = Settings.objects.all()[:1].get()
        sett.radarr_last_sync = datetime.now().strftime("%b %d %Y %H:%M:%S")
        sett.save()
        try:
            time.sleep(2)    # pause 5.5 seconds
            Logs.objects.create(log_type='Sync',log_category='System',log_message='Radarr Database sync finished',log_datetime=datetime.now().strftime("%b %d %Y %H:%M:%S"))
        except KeyError:
            pass

    return isSuccessful