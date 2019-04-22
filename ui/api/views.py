from jibarr.models import SiteSettings, Profile, ProfileRadarr, ProfileSonarr, ProfileLidarr, Logs, radarrMovie, RadarrMedia, sonarrShow, SonarrShowMedia, SonarrEpisodeMedia, ProfileSonarrEpisode
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from .serializers import SiteSettingsSerializer, ProfileSerializer, ProfileRadarrSerializer, ProfileSonarrSerializer, ProfileLidarrSerializer, LogsSerializer
from jibarr.copyTheFile import copyTheFile
from jibarr.copyTheShow import copyTheShow
from jibarr.RadarrSync import RadarrSync
from jibarr.SonarrSync import SonarrSync
from jibarr.SystemUpgrade import SystemUpgrade
from datetime import datetime
import os, os.path
from django.conf import settings

class SiteSettingsViewSet(viewsets.ModelViewSet):
    queryset = SiteSettings.objects.all()
    serializer_class = SiteSettingsSerializer
    def post(self, request, pk):
        if pk == 'update':
            request.session["prof_id"] = request.POST.get('profile_id')
            return Response("Ok")
        else:
            sett = SiteSettings.objects.all()[:1].get()
            sett.radarr_enabled = request.POST.get('radarr_enabled')
            sett.radarr_path = request.POST.get('radarr_path')
            sett.radarr_apikey = request.POST.get('radarr_apikey')
            sett.sonarr_enabled = request.POST.get('sonarr_enabled')
            sett.sonarr_path = request.POST.get('sonarr_path')
            sett.sonarr_apikey = request.POST.get('sonarr_apikey')
            sett.lidarr_enabled = request.POST.get('lidarr_enabled')
            sett.lidarr_path = request.POST.get('lidarr_path')
            sett.lidarr_apikey = request.POST.get('lidarr_apikey')
            sett.save()
            try:
                Logs.objects.create(log_type='Update',log_category='Settings',log_message='Settings updated.',log_datetime=datetime.now().strftime("%b %d %Y %H:%M:%S"))
            except KeyError:
                pass
            return Response("Ok")

class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    def post(self, request, pk):
        if pk =='add':
            pname = request.POST.get('profile_name')
            plr = request.POST.get('profile_lastRun')
            p = Profile.objects.create(profile_name=pname,profile_lastRun=plr)
            try:
                Logs.objects.create(log_type='Add',log_category='Profile',log_message='Added ' + pname,log_datetime=datetime.now().strftime("%b %d %Y %H:%M:%S"))
            except KeyError:
                pass
        elif pk == 'delete':
            pid = int(request.POST.get('profile_id'))
            p = Profile.objects.get(id=pid)
            pname = p.profile_name
            p.delete()
            try:
                Logs.objects.create(log_type='Add',log_category='Profile',log_message='Delete ' + pname,log_datetime=datetime.now().strftime("%b %d %Y %H:%M:%S"))
            except KeyError:
                pass
        return Response("Ok")

class ProfileRadarrViewSet(viewsets.ModelViewSet):
    queryset = ProfileRadarr.objects.all()
    serializer_class = ProfileRadarrSerializer
    ret = ""
    def post(self, request, pk):
        if pk == 'add':
            pid = request.POST.get('profile_id')
            rid = request.POST.get('radarr_id')
            rt = request.POST.get('radarr_title')
            pr = ProfileRadarr.objects.create(profile_id=pid,radarr_id=rid,lastRun='Jan 01 1970 23:59:59')
            pr.save()
            ret = pr.pk
            try:
                Logs.objects.create(log_type='Add',log_category='Radarr',log_message='Added ' + rt + ' to ProfileID ' + pid,log_datetime=datetime.now().strftime("%b %d %Y %H:%M:%S"))
            except KeyError:
                pass
        if pk == 'delete':
            prid = int(request.POST.get('prid'))
            pid = request.POST.get('profile_id')
            rt = request.POST.get('radarr_title')
            pr = ProfileRadarr.objects.get(id=prid)
            pr.delete()
            ret = "DelOK"
            try:
                Logs.objects.create(log_type='Delete',log_category='Radarr',log_message='Deleted ' + rt + ' from ProfileID ' + pid,log_datetime=datetime.now().strftime("%b %d %Y %H:%M:%S"))
            except KeyError:
                pass
        return Response(ret)

class ProfileSonarrViewSet(viewsets.ModelViewSet):
    queryset = ProfileSonarr.objects.all()
    serializer_class = ProfileSonarrSerializer
    ret = ""
    def post(self, request, pk):
        pid = request.POST.get('profile_id')
        sid = request.POST.get('sonarr_id')
        st = request.POST.get('sonarr_title')
        
        if pk == 'add':
            ps = ProfileSonarr.objects.create(profile_id=pid,sonarr_id=sid,lastRun='Jan 01 1970 23:59:59')
            ps.save()
            ret = ps.pk
            try:
                Logs.objects.create(log_type='Add',log_category='Sonarr',log_message='Sonarr entry added ' + st + ' to ProfileID ' + pid,log_datetime=datetime.now().strftime("%b %d %Y %H:%M:%S"))
            except KeyError:
                pass
        if pk == 'delete':
            ps = ProfileSonarr.objects.filter(sonarr_id=sid,profile_id=pid)
            ps.delete()
            ret = "DelOK"
            try:
                Logs.objects.create(log_type='Delete',log_category='Sonarr',log_message='Sonarr entry deleted ' + st + ' from ProfileID ' + pid,log_datetime=datetime.now().strftime("%b %d %Y %H:%M:%S"))
            except KeyError:
                pass
        return Response(ret)

class ProfileLidarrViewSet(viewsets.ModelViewSet):
    queryset = ProfileLidarr.objects.all()
    serializer_class = ProfileLidarrSerializer
    def post(self, request, pk):
        if pk == 'add':
            pid = request.POST.get('profile_id')
            lid = request.POST.get('lidarr_id')
            pl = ProfileLidarr.objects.create(profile_id=pid,lidarr_id=lid,lastRun='Jan 01 1970 23:59:59')
            try:
                Logs.objects.create(log_type='Add',log_category='Lidarr',log_message='Lidarr entry added',log_datetime=datetime.now().strftime("%b %d %Y %H:%M:%S"))
            except KeyError:
                pass
        if pk == 'delete':
            plid = int(request.POST.get('plid'))
            pl = ProfileLidarr.objects.get(id=plid)
            pl.delete()
            try:
                Logs.objects.create(log_type='Delete',log_category='Lidarr',log_message='Lidarr entry added',log_datetime=datetime.now().strftime("%b %d %Y %H:%M:%S"))
            except KeyError:
                pass
        return Response("Ok")

@api_view(['GET', 'POST'])
def RunSync(request):
    idList = request.POST.getlist('idlist[]')
    destDir = request.POST.get('destDir')
    prof_id = request.POST.get('prof_id')
    prof = Profile.objects.get(id=prof_id)
    try:
        Logs.objects.create(log_type='Sync',log_category='System',log_message='Sync initiated for Profile ' + prof.profile_name,log_datetime=datetime.now().strftime("%b %d %Y %H:%M:%S"))
    except KeyError:
        pass
    copyTheFile(idList, destDir, prof_id)
    try:
        Logs.objects.create(log_type='Sync',log_category='System',log_message='Sync completed for Profile ' + prof.profile_name,log_datetime=datetime.now().strftime("%b %d %Y %H:%M:%S"))
    except KeyError:
        pass
    try:
        prof.profile_lastPath = destDir
        prof.save()
    except KeyError:
        pass
    return Response("OK")

class LogsViewSet(viewsets.ModelViewSet):
    queryset = Logs.objects.all()
    serializer_class = LogsSerializer
    def post(self, request, pk):
        if pk == 'clear':
            Logs.objects.all().delete()
        return Response("Ok")

@api_view(['GET', 'POST'])
def GetFolders(request):
    startDir = request.POST.get(r'startDir')
    subDirs = []
    for d in os.listdir(startDir):
        if os.path.isdir(os.path.join(startDir,d)):
            subDirs.append(d)
    return Response(subDirs)

@api_view(['GET', 'POST'])
def dbsync(request):
    sourceSync = 'all'
    try:
        if(request.POST.get("sourceSync")):
            sourceSync = request.POST.get("sourceSync")
    except KeyError:
        pass
    if(sourceSync=='radarr'):
        RadarrSync(False)
    if(sourceSync=='radarr_force'):
        RadarrSync(True)
    if(sourceSync=='sonarr'):
        SonarrSync(False)
    if(sourceSync=='sonarr_force'):
        SonarrSync(True)
    return Response("OK")
        
@api_view(['GET', 'POST'])
def scheduler(request):
    runType = 'none'
    response = "Failed"
    try:
        runType = request.POST.get("runType")
        if runType=='enable':
            sett = SiteSettings.objects.all()[:1].get()
            sett.scheduler_enabled = 1
            sett.save()
            response = "OK"
        elif runType=='disable':
            sett = SiteSettings.objects.all()[:1].get()
            sett.scheduler_enabled = 0
            sett.save()
            response = "OK"
        elif runType=='radarr':
            # run the radarr sync
            response = "OK"
    except:
        pass
    return Response(response)

@api_view(['GET', 'POST'])
def marksynced(request):
    try:
        # call to update everything with today's date.
        try:
            Logs.objects.create(log_type='Sync',log_category='System',log_message='Bulk override of Sync Date initiated.',log_datetime=datetime.now().strftime("%b %d %Y %H:%M:%S"))
        except:
            pass
        prof_id = request.POST.get('prof_id')
        #prof = Profile.objects.get(id=prof_id)
        prlist = ProfileRadarr.objects.filter(profile_id=prof_id)
        for pr in prlist:
            pr.lastRun = datetime.now().strftime("%b %d %Y %H:%M:%S")
            pr.save()
        try:
            Logs.objects.create(log_type='Sync',log_category='System',log_message='Bulk override of Sync Date completed.',log_datetime=datetime.now().strftime("%b %d %Y %H:%M:%S"))
        except:
            pass
    except:
        pass

    return Response("OK")

@api_view(['GET', 'POST'])
def runUpgradeProcess(request):
    isSuccessfull = True
    try:
        toVer = request.POST.get("toVer")
        isSuccessfull = SystemUpgrade(toVer)
    except:
        pass

    if isSuccessfull:
        return Response("OK")
    else:
        return Response("FAIL")

@api_view(['GET', 'POST'])
def upgrades(request):
    runType = 'none'
    response = "Failed"
    try:
        runType = request.POST.get("runType")
        if runType=='enable':
            sett = SiteSettings.objects.all()[:1].get()
            sett.upgrades_enabled = 1
            sett.save()
            response = "OK"
        elif runType=='disable':
            sett = SiteSettings.objects.all()[:1].get()
            sett.upgrades_enabled = 0
            sett.save()
            response = "OK"
    except:
        pass
    return Response(response)

@api_view(['GET', 'POST'])
def markmoviesmonitored(request):
    try:
        prof_id = request.POST.get('prof_id')
        prof = Profile.objects.get(id=prof_id)
        rmList = RadarrMedia.objects.all()
        prList = ProfileRadarr.objects.filter(profile_id=prof_id)
        
        try:
            Logs.objects.create(log_type='Sync',log_category='System',log_message='Bulk override, mark all Monitored for Profile (' + prof.profile_name + ') initiated.',log_datetime=datetime.now().strftime("%b %d %Y %H:%M:%S"))
        except:
            pass

        isSuccessfull = False
        try:
            for rm in rmList:
                found = False
                for pr in prList:
                    if pr.radarr_id == rm.radarr_id:
                        found = True
                        break
                if found == False:
                    # add it
                    pr = ProfileRadarr.objects.create(profile_id=prof_id,radarr_id=rm.radarr_id,lastRun="Jan 01 1970 23:59:59")
                    pr.save()
            isSuccessfull = True
        except:
            isSuccessfull = False
            pass

        try:
            if isSuccessfull:
                prof = Profile.objects.get(id=prof_id)
                prof.profile_lastRun = datetime.now().strftime("%b %d %Y %H:%M:%S")
                prof.save()
                Logs.objects.create(log_type='Sync',log_category='System',log_message='Bulk override, mark all Monitored for Profile (' + prof.profile_name + ') completed.',log_datetime=datetime.now().strftime("%b %d %Y %H:%M:%S"))
            else:
                Logs.objects.create(log_type='Sync',log_category='System',log_message='Bulk override, mark all Monitored for Profile (' + prof.profile_name + ') FAILED.',log_datetime=datetime.now().strftime("%b %d %Y %H:%M:%S"))
        except:
            pass
    except:
        pass

    return Response("OK")

@api_view(['GET', 'POST'])
def automonitor(request):
    runType = 'none'
    response = "Failed"
    try:
        runType = request.POST.get("runType")
        if runType=='enable':
            prof_id = request.POST.get('prof_id')
            prof = Profile.objects.get(id=prof_id)
            prof.radarr_monitor = 1
            prof.save()
            response = "OK"
            Logs.objects.create(log_type='System',log_category='System',log_message='Automonitor new movies for Profile (' + prof.profile_name + ') enabled.',log_datetime=datetime.now().strftime("%b %d %Y %H:%M:%S"))
        elif runType=='disable':
            prof_id = request.POST.get('prof_id')
            prof = Profile.objects.get(id=prof_id)
            prof.radarr_monitor = 0
            prof.save()
            response = "OK"
            Logs.objects.create(log_type='System',log_category='System',log_message='Automonitor new movies for Profile (' + prof.profile_name + ') disabled.',log_datetime=datetime.now().strftime("%b %d %Y %H:%M:%S"))
    except:
        pass
    return Response(response)

@api_view(['GET', 'POST'])
def changeRadarrStatus(request):
    runType = 'none'
    response = "Failed"
    try:
        runType = request.POST.get("runType")
        if runType=='enable':
            settings.isConnected = True
            response = "OK"
            Logs.objects.create(log_type='System',log_category='Radarr',log_message='Radarr Connection Status changed - Connected.',log_datetime=datetime.now().strftime("%b %d %Y %H:%M:%S"))
        elif runType=='disable':
            settings.isConnected = False
            response = "OK"
            Logs.objects.create(log_type='System',log_category='Radarr',log_message='Radarr Connection Status changed - Disconnected.',log_datetime=datetime.now().strftime("%b %d %Y %H:%M:%S"))
    except:
        pass
    return Response(response)

@api_view(['GET', 'POST'])
def changeSonarrStatus(request):
    runType = 'none'
    response = "Failed"
    try:
        runType = request.POST.get("runType")
        if runType=='enable':
            settings.isSonarrConnected = True
            response = "OK"
            Logs.objects.create(log_type='System',log_category='Sonarr',log_message='Sonarr Connection Status changed - Connected.',log_datetime=datetime.now().strftime("%b %d %Y %H:%M:%S"))
        elif runType=='disable':
            settings.isSonarrConnected = False
            response = "OK"
            Logs.objects.create(log_type='System',log_category='Sonarr',log_message='Sonarr Connection Status changed - Disconnected.',log_datetime=datetime.now().strftime("%b %d %Y %H:%M:%S"))
    except:
        pass
    return Response(response)

@api_view(['GET', 'POST'])
def skipEpisode(request):
    runType = 'none'
    response = "Failed"

    try:
        prof_id = request.POST.get('prof_id')
        prof = Profile.objects.get(id=prof_id)
        sid = request.POST.get('episodeId')
        sem = SonarrEpisodeMedia.objects.get(sonarr_id=sid)
        ser = SonarrShowMedia.objects.get(sonarr_id=sem.seriesId)
        runType = request.POST.get("runType")
        if runType=='skip':
            # check if it's already in the PSE table
            if ProfileSonarrEpisode.objects.filter(profile_id=prof_id,sonarr_id=sid).count() == 1:
                pse = ProfileSonarrEpisode.objects.get(profile_id=prof_id,sonarr_id=sid)
                #if pse:
                # if yes, update runDate to 2099
                pse.lastRun = "Dec 31 2099 23:59:59"
                pse.save()
            else:
                # if no, insert it with 2099
                ProfileSonarrEpisode.objects.create(profile_id=prof_id,sonarr_id=sid,lastRun="Dec 31 2099 23:59:59")
            response = "OK"
            try:
                Logs.objects.create(log_type='Add',log_category='Sonarr',log_message='Sonarr ' + ser.title + '[' + str(sem.episodeNumber) + ']' + sem.title + ' skipped for ' + prof.profile_name + '.',log_datetime=datetime.now().strftime("%b %d %Y %H:%M:%S"))
            except:
                pass
        elif runType=='unskip':
            # get the PSE and change last run date to 1970
            pse = ProfileSonarrEpisode.objects.get(profile_id=prof_id,sonarr_id=sid)
            pse.lastRun = "Jan 01 1970 23:59:59"
            pse.save()
            response = "OK"
            try:
                Logs.objects.create(log_type='Add',log_category='Sonarr',log_message='Sonarr ' + ser.title + '[' + sem.episodeNumber + ']' + sem.title + ' un-skipped for profile ' + prof.profile_name + '.',log_datetime=datetime.now().strftime("%b %d %Y %H:%M:%S"))
            except:
                pass
    except Exception as e:
        try:
            Logs.objects.create(log_type='ERROR',log_category='Sonarr',log_message='Sonarr skipEpisode error [' + e + '.',log_datetime=datetime.now().strftime("%b %d %Y %H:%M:%S"))
        except:
            pass
        pass
    return Response(response)

@api_view(['GET', 'POST'])
def RunSyncShows(request):
    idList = request.POST.getlist('idlist[]')
    destDir = request.POST.get('destDir')
    prof_id = request.POST.get('prof_id')
    prof = Profile.objects.get(id=prof_id)
    create_show_fldr = request.POST.get("create_show_fldr")
    create_season_fldr = request.POST.get("create_season_fldr")
    
    try:
        Logs.objects.create(log_type='Sync',log_category='System',log_message='Sonarr Sync initiated for Profile ' + prof.profile_name,log_datetime=datetime.now().strftime("%b %d %Y %H:%M:%S"))
    except KeyError:
        pass
    copyTheShow(idList, destDir, prof_id, create_show_fldr, create_season_fldr)
    try:
        Logs.objects.create(log_type='Sync',log_category='System',log_message='Sonarr Sync completed for Profile ' + prof.profile_name,log_datetime=datetime.now().strftime("%b %d %Y %H:%M:%S"))
    except KeyError:
        pass
    try:
        prof.profile_lastPath = destDir
        prof.save()
    except KeyError:
        pass
    return Response("OK")

@api_view(['GET', 'POST'])
def markshowssynced(request):
    try:
        # call to update everything with today's date.
        try:
            Logs.objects.create(log_type='Sync',log_category='System',log_message='Bulk override of Sync Date initiated.',log_datetime=datetime.now().strftime("%b %d %Y %H:%M:%S"))
        except:
            pass
        prof_id = request.POST.get('prof_id')

        profile_sonarr_show_list = ProfileSonarr.objects.filter(profile_id=prof_id)
        for pss in profile_sonarr_show_list:
            sel = SonarrEpisodeMedia.objects.filter(seriesId=pss.sonarr_id)
            for se in sel:
                # check if the episode is monitored
                if ProfileSonarrEpisode.objects.filter(profile_id=prof_id,sonarr_id=se.sonarr_id).count() == 1:
                    pse = ProfileSonarrEpisode.objects.get(profile_id=prof_id,sonarr_id=se.sonarr_id)
                    if pse:
                        pse.lastRun = datetime.now().strftime("%b %d %Y %H:%M:%S")
                        pse.save()
                else:
                    # not in PSE, add it to sync list
                    pse = ProfileSonarrEpisode.objects.create(profile_id=prof_id,sonarr_id=se.sonarr_id,lastRun=datetime.now().strftime("%b %d %Y %H:%M:%S"))

        try:
            Logs.objects.create(log_type='Sync',log_category='System',log_message='Bulk override of Sync Date completed.',log_datetime=datetime.now().strftime("%b %d %Y %H:%M:%S"))
        except:
            pass
    except:
        pass

    return Response("OK")

