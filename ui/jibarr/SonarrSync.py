import os, shutil, json, time
from jibarr.models import SiteSettings, Logs, SonarrShowMedia, Profile, ProfileSonarr, SonarrEpisodeMedia
from urllib.request import urlopen
from datetime import datetime

def SonarrSync(forceload):
    try:
        Logs.objects.create(log_type='Sync',log_category='System',log_message='Sonarr Database sync started',log_datetime=datetime.now().strftime("%b %d %Y %H:%M:%S"))
    except KeyError:
        pass
    isSuccessful = False
    system_settings = SiteSettings.objects.all()[:1].get()

    # call to SONARR and read JSON
    data = urlopen(system_settings.sonarr_path + "/api/series/?apikey=" + system_settings.sonarr_apikey).read()
    output = json.loads(data)

    if forceload:
        # PURGE THE DATABASE
        SonarrShowMedia.objects.all().delete()
    
    # iterate JSON 
    for var in output:
        try:
            if forceload:
                # do an INSERT on every record
               
                ssm = SonarrShowMedia
                ssm.sonarr_id = var['id']
                ssm.title = var['title']
                ssm.description = var['overview']
                ssm.title_slug = var['titleSlug']
                ssm.year = var['year']
                ssm.path = var['path']
                ssm.lastInfoSync = var['lastInfoSync'][:10]
                ssm.rating = var["ratings"]["value"]
                ssm.tvdbId = ""
                try:
                    ssm.tvdbId = var["tvdbId"]
                except:
                    pass
                ssm.tvRageId = ""
                try:
                    ssm.tvRageId = var["tvRageId"]
                except:
                    pass
                ssm.tvMazeId = ""
                try:
                    ssm.tvMazeId = var["tvMazeId"]
                except:
                    pass
                ssm.imdbId = ""
                try:
                    ssm.imdbId = var["imdbId"]
                except:
                    pass
                ssm.seasonCount = var['seasonCount']
                ssm.episodeCount = var['episodeCount']
                ssm.episodeFileCount = var['episodeFileCount']

                SonarrShowMedia.objects.create(sonarr_id = ssm.sonarr_id,title = ssm.title,title_slug = ssm.title_slug,year = ssm.year,path = ssm.path,lastInfoSync = ssm.lastInfoSync,rating = ssm.rating,tvdbId = ssm.tvdbId,tvRageId = ssm.tvRageId,tvMazeId = ssm.tvMazeId,imdbId = ssm.imdbId,seasonCount = ssm.seasonCount,episodeCount = ssm.episodeCount, description = ssm.description, episodeFileCount = ssm.episodeFileCount)
                isSuccessful = True
                
                ## TODO - Run the insert for all profiles with auto-add
                #for profId in aaProfId:
                #    ProfileRadarr.objects.create(profile_id=profId,radarr_id=var['id'],lastRun="Jan 01 1970 23:59:59")
            else:
                # check ID against DB
                try:
                    ssm = SonarrShowMedia.objects.get(sonarr_id=var['id'])
                    ssm.doesExist = True
                except:
                    ssm = SonarrShowMedia
                    ssm.doesExist = False
                    pass

                wasUpdated = False
                ## if exist - Update
                if ssm.doesExist:
                    
                    if ssm.title != var['title']:
                        wasUpdated = True
                        ssm.title = var['title']
                    if ssm.title_slug != var['titleSlug']:
                        wasUpdated = True
                        ssm.title_slug = var['titleSlug']
                    if ssm.description != var['overview']:
                        wasUpdated = True
                        ssm.description = var['overview']
                    if ssm.year != var['year']:
                        wasUpdated = True
                        ssm.year = var['year']
                    if ssm.path != var['path']:
                        wasUpdated = True
                        ssm.path = var['path']
                    if ssm.lastInfoSync != var['lastInfoSync'][:10]:
                        wasUpdated = True
                        ssm.lastInfoSync = var['lastInfoSync'][:10]
                    if ssm.rating != var["ratings"]["value"]:
                        #wasUpdated = True
                        ssm.rating = var["ratings"]["value"]
                    if ssm.tvdbId != var["tvdbId"]:
                        wasUpdated = True
                        ssm.tvdbId = var["tvdbId"]
                    if ssm.tvRageId != var["tvRageId"]:
                        wasUpdated = True
                        ssm.tvRageId = var["tvRageId"]
                    if ssm.tvMazeId != var["tvMazeId"]:
                        wasUpdated = True
                        ssm.tvMazeId = var["tvMazeId"]
                    if ssm.imdbId != var["imdbId"]:
                        wasUpdated = True
                        ssm.imdbId = var["imdbId"]
                    if ssm.seasonCount != var['seasonCount']:
                        wasUpdated = True
                        ssm.seasonCount = var['seasonCount']
                    if ssm.episodeCount != var['episodeCount']:
                        wasUpdated = True
                        ssm.episodeCount = var['episodeCount']
                    if ssm.episodeFileCount != var['episodeFileCount']:
                        wasUpdated = True
                        ssm.episodeFileCount = var['episodeFileCount']
                    if wasUpdated:
                        try:
                            Logs.objects.create(log_type='Sync',log_category='System',log_message='Updated ' + ssm.title + ' from Sonarr.',log_datetime=datetime.now().strftime("%b %d %Y %H:%M:%S"))
                        except:
                            pass
                        ssm.save()
                    isSuccessful = True
                else:
                    ## if not exist - Insert
                    ssm = SonarrShowMedia
                    ssm.sonarr_id = var['id']
                    ssm.title = var['title']
                    ssm.title_slug = var['titleSlug']
                    ssm.description = var['overview']
                    ssm.year = var['year']
                    ssm.path = var['path']
                    ssm.lastInfoSync = var['lastInfoSync'][:10]
                    ssm.rating = var["ratings"]["value"]
                    ssm.tvdbId = ""
                    try:
                        ssm.tvdbId = var["tvdbId"]
                    except:
                        pass
                    ssm.tvRageId = ""
                    try:
                        ssm.tvRageId = var["tvRageId"]
                    except:
                        pass
                    ssm.tvMazeId = ""
                    try:
                        ssm.tvMazeId = var["tvMazeId"]
                    except:
                        pass
                    ssm.imdbId = ""
                    try:
                        ssm.imdbId = var["imdbId"]
                    except:
                        pass
                    ssm.seasonCount = var['seasonCount']
                    ssm.episodeCount = var['episodeCount']
                    ssm.episodeFileCount = var['episodeFileCount']
                    
                    SonarrShowMedia.objects.create(sonarr_id = ssm.sonarr_id,title = ssm.title,title_slug = ssm.title_slug,year = ssm.year,path = ssm.path,lastInfoSync = ssm.lastInfoSync,rating = ssm.rating,tvdbId = ssm.tvdbId,tvRageId = ssm.tvRageId,tvMazeId = ssm.tvMazeId,imdbId = ssm.imdbId,seasonCount = ssm.seasonCount,episodeCount = ssm.episodeCount, description = ssm.description, episodeFileCount = ssm.episodeFileCount)
                    try:
                        Logs.objects.create(log_type='Sync',log_category='System',log_message='Added ' + ssm.title + ' from Sonarr',log_datetime=datetime.now().strftime("%b %d %Y %H:%M:%S"))
                    except:
                        pass
                    isSuccessful = True

                    ## TODO - Run the insert for all profiles with auto-add
                    #for profId in aaProfId:
                    #    ProfileRadarr.objects.create(profile_id=profId,radarr_id=var['id'],lastRun="Jan 01 1970 23:59:59")
            
        except:
            pass

    if isSuccessful:
        ############################################### update settings last sync date
        sett = SiteSettings.objects.all()[:1].get()
        sett.sonarr_last_sync = datetime.now().strftime("%b %d %Y %H:%M:%S")
        sett.save()
        try:
            time.sleep(2)    # pause 2 seconds
            Logs.objects.create(log_type='Sync',log_category='System',log_message='Sonarr Database sync finished',log_datetime=datetime.now().strftime("%b %d %Y %H:%M:%S"))
        except KeyError:
            pass
    else:
        try:
            time.sleep(2)    # pause 5.5 seconds
            Logs.objects.create(log_type='Sync',log_category='System',log_message='Sonarr Database sync failed',log_datetime=datetime.now().strftime("%b %d %Y %H:%M:%S"))
        except KeyError:
            pass
    # do Series Episode loop
    if isSuccessful:
        isSuccessful = LoopSeries(forceload)

    ## do Episode loop
    #if isSuccessful:
    #    isSuccessful = LoopEpisodes()

    return isSuccessful

def LoopSeries(forceload):
    try:
        Logs.objects.create(log_type='Sync',log_category='System',log_message='Sonarr Episode sync started',log_datetime=datetime.now().strftime("%b %d %Y %H:%M:%S"))
    except:
        pass
    isSuccessful = True

    system_settings = SiteSettings.objects.all()[:1].get()

    if forceload:
        # PURGE THE DATABASE
        SonarrEpisodeMedia.objects.all().delete()

    for var in SonarrShowMedia.objects.all():
        try:
            # call to EpisodeFile for each series sonarr_id
            # http://localhost:8989/api/Episode/?seriesId=1&apikey=4477ca27f3b54214b3ec6c26b469d821
            urlString = system_settings.sonarr_path + "/api/Episode/?seriesId=" + str(var.sonarr_id) + "&apikey=" + system_settings.sonarr_apikey
            data = urlopen(urlString).read()
            output = json.loads(data)

            if forceload:
                for var in output:
                    if var["hasFile"]:
                        sem = SonarrEpisodeMedia
                        sem.sonarr_id = var["id"]
                        sem.seriesId = var["seriesId"]
                        sem.episodeNumber = var["episodeNumber"]
                        sem.title = var["title"]
                        sem.seasonNumber = var["seasonNumber"]
                        sem.path = var["episodeFile"]["path"]
                        sem.dateAdded = var['episodeFile']['dateAdded'][:10] + " " + var['episodeFile']['dateAdded'][11:16]
                        sem.quality = var["episodeFile"]["quality"]["quality"]["name"]
                        sem.description = ""
                        try:
                            sem.description = var["overview"]
                        except:
                            pass
                        sem.airDate = var["airDate"]
                        sem.size = var["episodeFile"]["size"]
                        SonarrEpisodeMedia.objects.create(sonarr_id=sem.sonarr_id, seriesId = sem.seriesId, seasonNumber = sem.seasonNumber, path = sem.path, dateAdded = sem.dateAdded, episodeNumber = sem.episodeNumber, title = sem.title, quality = sem.quality, description = sem.description, airDate = sem.airDate, size = sem.size)
            else:
                # update episodes
                for var in output:
                    sem = SonarrEpisodeMedia
                    if var["hasFile"]:
                        # check if exists
                        
                        try:
                            sem = SonarrEpisodeMedia.objects.get(sonarr_id=var["id"])
                            sem.doesExist = True
                        except:
                            sem = SonarrEpisodeMedia
                            sem.doesExist = False
                            pass
                        
                        if sem.doesExist:
                            wasUpdated = False
                            if sem.title != var['title']:
                                wasUpdated = True
                                sem.title = var['title']
                            #seriesId = models.IntegerField()
                            if sem.seriesId != var['seriesId']:
                                wasUpdated = True
                                sem.seriesId = var['seriesId']
                            #episodeNumber = models.IntegerField()
                            if sem.episodeNumber != var['episodeNumber']:
                                wasUpdated = True
                                sem.episodeNumber = var['episodeNumber']
                            #seasonNumber = models.IntegerField()
                            if sem.seasonNumber != var['seasonNumber']:
                                wasUpdated = True
                                sem.seasonNumber = var['seasonNumber']
                            #path = models.CharField(max_length=200)
                            if sem.path != var['episodeFile']['path']:
                                wasUpdated = True
                                sem.path = var['episodeFile']['path']
                            #dateAdded = models.CharField(max_length=200)
                            if sem.dateAdded != var['episodeFile']['dateAdded'][:10] + " " + var['episodeFile']['dateAdded'][11:16]:
                                wasUpdated = True
                                sem.dateAdded = var['episodeFile']['dateAdded'][:10] + " " + var['episodeFile']['dateAdded'][11:16]
                            #quality = models.CharField(max_length=200)
                            if sem.quality != var['episodeFile']['quality']['quality']['name']:
                                wasUpdated = True
                                sem.quality = var['episodeFile']['quality']['quality']['name']
                            #description = models.CharField(max_length=2000)
                            try:
                                if sem.description != var['overview']:
                                    wasUpdated = True
                                    sem.description = var['overview']
                            except:
                                sem.description = ''
                                pass
                            #airDate = models.CharField(max_length=200)
                            if sem.airDate != var['airDate']:
                                wasUpdated = True
                                sem.airDate = var['airDate']
                            #size = models.IntegerField()
                            if sem.size != var['episodeFile']['size']:
                                wasUpdated = True
                                sem.size = var['episodeFile']['size']
                            # SAVE
                            if wasUpdated:
                                try:
                                    Logs.objects.create(log_type='Sync',log_category='System',log_message='Updated ' + sem.title + '[' + str(sem.seasonNumber) + '/' + str(sem.episodeNumber) + '] from Sonarr.',log_datetime=datetime.now().strftime("%b %d %Y %H:%M:%S"))
                                except:
                                    pass
                                sem.save()
                            isSuccessful = True
                        else:
                            #seriesId = models.IntegerField()
                            #episodeNumber = models.IntegerField()
                            #title = models.CharField(max_length=200)
                            #seasonNumber = models.IntegerField()
                            #path = models.CharField(max_length=200)
                            #dateAdded = models.CharField(max_length=200)
                            #quality = models.CharField(max_length=200)
                            #description = models.CharField(max_length=2000)
                            semDescription = ''
                            try:
                                semDescription = var['overview']
                            except:
                                pass
                            #airDate = models.CharField(max_length=200)
                            #size = models.IntegerField()
                            # CREATE
                            sem = SonarrEpisodeMedia.objects.create(sonarr_id=var['id'],seriesId=var['seriesId'],episodeNumber=var['episodeNumber'],title=var['title'],seasonNumber=var['seasonNumber'],path=var['episodeFile']['path'],dateAdded=var['episodeFile']['dateAdded'][:10] + " " + var['episodeFile']['dateAdded'][11:16],quality=var['episodeFile']['quality']['quality']['name'],description=semDescription,airDate=var['airDate'],size=var['episodeFile']['size'])
                        
        except Exception as e:
            Logs.objects.create(log_type='Sync',log_category='System',log_message='Sonarr Episode update failed: ' + str(var["id"]) + ' -- ',log_datetime=datetime.now().strftime("%b %d %Y %H:%M:%S"))
            pass
    try:
        Logs.objects.create(log_type='Sync',log_category='System',log_message='Sonarr Episode sync ended',log_datetime=datetime.now().strftime("%b %d %Y %H:%M:%S"))
    except:
        pass
    return isSuccessful

def LoopEpisodes():
    system_settings = SiteSettings.objects.all()[:1].get()
    isSuccessful = True
    try:
        for sem in SonarrEpisodeMedia.objects.all():
            #http://localhost:8989/api/episode/1/?apikey=4477ca27f3b54214b3ec6c26b469d821
            urlString = system_settings.sonarr_path + "/api/episode/" + str(sem.sonarr_id) + "/?apikey=" + system_settings.sonarr_apikey
            data = urlopen(urlString).read()
            output = json.loads(data)
            sem.episodeNumber = output["episodeNumber"]
            sem.title = output["title"]
            #sem.quality = output["episodeFile"]["quality"]["quality"]["name"]
            try:
                sem.description = output["overview"]
            except:
                pass
            try:
                sem.airDate = output["airDate"]
            except:
                pass
            #sem.size = output["episodeFile"]["size"]
            sem.save()
    except Exception as e:
        Logs.objects.create(log_type='Sync',log_category='System',log_message='Sonarr Episode update failed: ' + e,log_datetime=datetime.now().strftime("%b %d %Y %H:%M:%S"))
        pass
    return isSuccessful