import os, shutil, json
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
        if forceload:
            # do an INSERT on every record
            rm = RadarrMedia
            rm.radarr_id = var['id']
            rm.title = var['title']
            rm.title_slug = var['titleSlug']
            try:
                rm.release_date = var['inCinemas'][:10]
            except KeyError:
                rm.release_date = ""

            if var['hasFile']:    
                rm.folder_name = var["folderName"]
                rm.size = var["movieFile"]["size"]
                rm.file_name = var["movieFile"]["relativePath"]
                rm.last_updt = var['movieFile']['dateAdded'][:10] + " " + var['movieFile']['dateAdded'][11:16]
            rm.rating = rm.rating = var["ratings"]["value"]
            try:
                rm.tmdbid = var["tmdbId"]
            except KeyError:
                rm.tmdbid = ""
                pass
            
            try:
                rm.imdbid = var["imdbId"]
            except KeyError:
                rm.imdbid = ""
                pass
            
            try:
                rm.youtube = var["youTubeTrailerId"]
            except KeyError:
                rm.youtube = ""
                pass
            
            try:
                rm.website = var["website"]
            except KeyError:
                rm.website = ""
                pass
            
            try:
                rm.quality = var["movieFile"]["quality"]["quality"]["name"]
            except KeyError:
                rm.quality = ""
                pass
            
            RadarrMedia.objects.create(radarr_id = rm.radarr_id,title = rm.title,title_slug = rm.title_slug,release_date = rm.release_date,folder_name = rm.folder_name,size = rm.size,file_name = rm.file_name,last_updt = rm.last_updt,rating = rm.rating,tmdbid = rm.tmdbid,imdbid = rm.imdbid,youtube = rm.youtube,website = rm.website,quality = rm.quality)
            #rm.save()
            isSuccessful = True

        else:
            # check ID against DB
            rm = RadarrMedia.objects.get(radarr_id=var['id'])

            ## if exist - Update
            if rm.id:
                rm.radarr_id = var['id']
                rm.title = var['title']
                rm.title_slug = var['titleSlug']
                try:
                    rm.release_date = var['inCinemas'][:10] # + " " + var['inCinemas'][11:16]
                except KeyError:
                    rm.release_date = ""

                if var['hasFile']:    
                    rm.folder_name = var["folderName"]
                    rm.size = var["movieFile"]["size"]
                    rm.file_name = var["movieFile"]["relativePath"]
                    rm.last_updt = var['movieFile']['dateAdded'][:10] + " " + var['movieFile']['dateAdded'][11:16]
                rm.rating = rm.rating = var["ratings"]["value"]
                try:
                    rm.tmdbid = var["tmdbId"]
                except KeyError:
                    rm.tmdbid = ""
                    pass
                
                try:
                    rm.imdbid = var["imdbId"]
                except KeyError:
                    rm.imdbid = ""
                    pass
                
                try:
                    rm.youtube = var["youTubeTrailerId"]
                except KeyError:
                    rm.youtube = ""
                    pass
                
                try:
                    rm.website = var["website"]
                except KeyError:
                    rm.website = ""
                    pass
                
                try:
                    rm.quality = var["movieFile"]["quality"]["quality"]["name"]
                except KeyError:
                    rm.quality = ""
                    pass
                
                #RadarrMedia.objects.create(radarr_id = rm.radarr_id,title = rm.title,title_slug = rm.title_slug,release_date = rm.release_date,folder_name = rm.folder_name,size = rm.size,file_name = rm.file_name,last_updt = rm.last_updt,rating = rm.rating,tmdbid = rm.tmdbid,imdbid = rm.imdbid,youtube = rm.youtube,website = rm.website,quality = rm.quality)
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
                except KeyError:
                    rm.release_date = ""

                if var['hasFile']:    
                    rm.folder_name = var["folderName"]
                    rm.size = var["movieFile"]["size"]
                    rm.file_name = var["movieFile"]["relativePath"]
                    rm.last_updt = var['movieFile']['dateAdded'][:10] + " " + var['movieFile']['dateAdded'][11:16]
                rm.rating = rm.rating = var["ratings"]["value"]
                try:
                    rm.tmdbid = var["tmdbId"]
                except KeyError:
                    rm.tmdbid = ""
                    pass
                
                try:
                    rm.imdbid = var["imdbId"]
                except KeyError:
                    rm.imdbid = ""
                    pass
                
                try:
                    rm.youtube = var["youTubeTrailerId"]
                except KeyError:
                    rm.youtube = ""
                    pass
                
                try:
                    rm.website = var["website"]
                except KeyError:
                    rm.website = ""
                    pass
                
                try:
                    rm.quality = var["movieFile"]["quality"]["quality"]["name"]
                except KeyError:
                    rm.quality = ""
                    pass
                
                RadarrMedia.objects.create(radarr_id = rm.radarr_id,title = rm.title,title_slug = rm.title_slug,release_date = rm.release_date,folder_name = rm.folder_name,size = rm.size,file_name = rm.file_name,last_updt = rm.last_updt,rating = rm.rating,tmdbid = rm.tmdbid,imdbid = rm.imdbid,youtube = rm.youtube,website = rm.website,quality = rm.quality)
                isSuccessful = True


    if isSuccessful:
        ############################################### update settings last sync date
        sett = Settings.objects.all()[:1].get()
        sett.RADARR_Last_Sync = datetime.now().strftime("%b %d %Y %H:%M:%S")
        sett.save()
        try:
            Logs.objects.create(log_type='Sync',log_category='System',log_message='Radarr Database sync finished',log_datetime=datetime.now().strftime("%b %d %Y %H:%M:%S"))
        except KeyError:
            pass

    return isSuccessful