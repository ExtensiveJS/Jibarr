from jibarr.models import Settings, Profile, ProfileRadarr, ProfileSonarr, ProfileLidarr, Logs, radarrMovie
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from .serializers import SettingsSerializer, ProfileSerializer, ProfileRadarrSerializer, ProfileSonarrSerializer, ProfileLidarrSerializer, LogsSerializer
from jibarr.copyTheFile import copyTheFile
from datetime import datetime
import os, os.path

class SettingsViewSet(viewsets.ModelViewSet):
    queryset = Settings.objects.all()
    serializer_class = SettingsSerializer
    def post(self, request, pk):
        if pk == 'update':
            request.session["prof_id"] = request.POST.get('profile_id')
            return Response("Ok")
        else:
            sett = Settings.objects.all()[:1].get()
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
    def post(self, request, pk):
        if pk == 'add':
            pid = request.POST.get('profile_id')
            sid = request.POST.get('sonarr_id')
            ps = ProfileSonarr.objects.create(profile_id=pid,sonarr_id=sid,lastRun='Jan 01 1970 23:59:59')
            try:
                Logs.objects.create(log_type='Add',log_category='Sonarr',log_message='Sonarr entry added',log_datetime=datetime.now().strftime("%b %d %Y %H:%M:%S"))
            except KeyError:
                pass
        if pk == 'delete':
            psid = int(request.POST.get('psid'))
            ps = ProfileSonarr.objects.get(id=psid)
            ps.delete()
            try:
                Logs.objects.create(log_type='Delete',log_category='Sonarr',log_message='Sonarr entry deleted',log_datetime=datetime.now().strftime("%b %d %Y %H:%M:%S"))
            except KeyError:
                pass
        return Response("Ok")

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
def DbSync(request):
    sourceSync = 'all'
    try:
        if(request.POST.get("sourceSync")):
            sourceSync = request.POST.get("sourceSync")
    except KeyError:
        pass
    if(sourceSync=='radarr'):
        # call out to Radarr
        # iterate the Radarr JSON
        # check against DB
        # Insert/Update DB
        return Response("OK")
        

