import os, shutil, json
from jibarr.models import SiteSettings, radarrMovie, ProfileRadarr, Profile, Logs
from urllib.request import urlopen
from datetime import datetime

def copyTheFile(idList, destDir, prof_id):
    isSuccessful = False
    try:
        isSuccessful = True

        for var in idList:
            system_settings = SiteSettings.objects.all()[:1].get()
            data = urlopen(system_settings.radarr_path + "/api/movie/" + str(var) + "?apikey=" + system_settings.radarr_apikey).read()
            output = json.loads(data) 
            startPoint = output['path'].rfind('\\')
            destSubDir = output['path'][startPoint + 1:]
            sourcePath = output['path'] + '\\' + output['movieFile']['relativePath']
            if os.path.exists(destDir + destSubDir) == False:
                os.makedirs(destDir + destSubDir)
            try:
                Logs.objects.create(log_type='Sync',log_category='System',log_message='Sync started for ' + output['movieFile']['relativePath'],log_datetime=datetime.now().strftime("%b %d %Y %H:%M:%S"))
            except KeyError:
                pass
            shutil.copy2(sourcePath,destDir + destSubDir + '\\' + output['movieFile']['relativePath'])
            try:
                Logs.objects.create(log_type='Sync',log_category='System',log_message='Sync finished for ' + output['movieFile']['relativePath'],log_datetime=datetime.now().strftime("%b %d %Y %H:%M:%S"))
            except KeyError:
                pass
            # call to update the ProfileRadarr table for this radarr_id and this profile_id
            profile_radarr = ProfileRadarr.objects.get(profile_id=prof_id,radarr_id=var)
            profile_radarr.lastRun = datetime.now().strftime("%b %d %Y %H:%M:%S")
            profile_radarr.save()
    except KeyError:
        isSuccessful = False
        pass

    if isSuccessful:
        # call to update the Profile to the new date/time stamp
        prof = Profile.objects.get(id=prof_id)
        prof.profile_lastRun = datetime.now().strftime("%b %d %Y %H:%M:%S")
        prof.save()
    return isSuccessful
    