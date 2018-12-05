import os, shutil, json
from MediaFileSync.models import Settings, radarrMovie, ProfileRadarr, Profile

from urllib.request import urlopen

def copyTheFile(idList, destDir, prof_id):
    isSuccessful = False
    try:
        isSuccessful = True
        # do the stuff here
        for var in idList:
            #pr = ProfileRadarr.objects.get(id=var)

            system_settings = Settings.objects.all()[:1].get()
            data = urlopen(system_settings.radarr_path + "/api/movie/" + str(var) + "?apikey=" + system_settings.radarr_apikey).read()
            output = json.loads(data) 
            startPoint = output['path'].rfind('\\')
            destSubDir = output['path'][startPoint + 1:]
            sourcePath = output['path'] + '\\' + output['movieFile']['relativePath']
            if os.path.exists(destDir + destSubDir) == False:
                os.makedirs(destDir + destSubDir)
            shutil.copy2(sourcePath,destDir + destSubDir + '\\' + output['movieFile']['relativePath'])
            # call to update the ProfileRadarr table for this radarr_id and this profile_id
            profile_radarr = ProfileRadarr.objects.get(profile_id=prof_id,radarr_id=var)
            profile_radarr.lastRun = 'Dec 04 2018 02:30PM'
            profile_radarr.save()
    except KeyError:
        isSuccessful = False
        pass

    if isSuccessful:
        # call to update the Profile to the new date/time stamp
        prof = Profile.objects.get(id=prof_id)
        prof.profile_lastRun = 'Dec 04 2018 02:30PM'
        prof.save()
    return isSuccessful
    