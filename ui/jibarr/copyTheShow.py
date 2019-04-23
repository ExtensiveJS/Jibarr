import os, shutil, json
from jibarr.models import SiteSettings, sonarrEpisode, SonarrEpisodeMedia, sonarrSeason, sonarrShow, ProfileSonarr, ProfileSonarrEpisode, Profile, Logs
from urllib.request import urlopen
from datetime import datetime

def copyTheShow(idList, destDir, prof_id, createShowFolder, createSeasonFolder):
    isSuccessful = False

    try:
        for var in idList:
            sem = SonarrEpisodeMedia.objects.get(sonarr_id=var)
            system_settings = SiteSettings.objects.all()[:1].get()
            urlString = system_settings.sonarr_path + "/api/episode/" + str(var) + "/?apikey=" + system_settings.sonarr_apikey
            data = urlopen(urlString).read()
            output = json.loads(data) 
            startPoint = output['episodeFile']['path'].rfind('\\')
            filename = output['episodeFile']['path'][startPoint + 1:]

            seriesFolder = ''
            seasonFolder = '\\Season '
            if sem.seasonNumber < 10:
                seasonFolder = seasonFolder + '0' + str(sem.seasonNumber)
            else:
                seasonFolder = seasonFolder + str(sem.seasonNumber)
            if createShowFolder == '1':
                #http://localhost:8989/api/series/1/?apikey=4477ca27f3b54214b3ec6c26b469d821
                urlString2 = system_settings.sonarr_path + "/api/series/" + str(sem.seriesId) + "/?apikey=" + system_settings.sonarr_apikey
                data2 = urlopen(urlString2).read()
                output2 = json.loads(data2) 
                startPoint2 = output2['path'].rfind('\\')
                seriesFolder = output2['path'][startPoint2 + 1:]
                if os.path.exists(destDir + seriesFolder) == False:
                    os.makedirs(destDir + seriesFolder)

            if createSeasonFolder == '1':
                if os.path.exists(destDir + seriesFolder + seasonFolder) == False:
                    os.makedirs(destDir + seriesFolder + seasonFolder)
            
            # time to copy the file
            copyTo = destDir
            if createShowFolder == '1':
                copyTo = copyTo + seriesFolder
            if createSeasonFolder == '1':
                copyTo = copyTo + seasonFolder
            shutil.copy2(output['episodeFile']['path'],copyTo + '\\' + filename)
            isSuccessful = True

            if ProfileSonarrEpisode.objects.filter(profile_id=prof_id,sonarr_id=var).count() == 1:
                pse = ProfileSonarrEpisode.objects.get(profile_id=prof_id,sonarr_id=var)
                pse.lastRun = datetime.now().strftime("%b %d %Y %H:%M:%S")
                pse.save()
            else:
                pse = ProfileSonarrEpisode.objects.create(profile_id=prof_id,sonarr_id=var,lastRun=datetime.now().strftime("%b %d %Y %H:%M:%S"))
                pse.save()

    except:
        isSuccessful = False
        pass

    if isSuccessful:
        # call to update the Profile to the new date/time stamp
        prof = Profile.objects.get(id=prof_id)
        prof.sonarr_lastRun = datetime.now().strftime("%b %d %Y %H:%M:%S")
        prof.save()
    return isSuccessful