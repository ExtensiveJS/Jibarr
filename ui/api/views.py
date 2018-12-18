from jibarr.models import Settings, Profile, ProfileRadarr, ProfileSonarr, ProfileLidarr, Logs
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from .serializers import SettingsSerializer, ProfileSerializer, ProfileRadarrSerializer, ProfileSonarrSerializer, ProfileLidarrSerializer, LogsSerializer
from jibarr.copyTheFile import copyTheFile
from datetime import datetime

#class SettingsViewSet(viewsets.ModelViewSet):
#    """
#    API endpoint that allows Settings to be viewed or edited.
#    """
#    queryset = Settings.objects.all()
#    serializer_class = SettingsSerializer

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
            return Response("Ok")

class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    def post(self, request, pk):
        if pk =='add':
            pname = request.POST.get('profile_name')
            plr = request.POST.get('profile_lastRun')
            p = Profile.objects.create(profile_name=pname,profile_lastRun=plr)
        elif pk == 'delete':
            pid = int(request.POST.get('profile_id'))
            p = Profile.objects.get(id=pid)
            p.delete()
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
            pr = ProfileRadarr.objects.create(profile_id=pid,radarr_id=rid,lastRun='Jan 01 1970 11:59PM')
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
            ps = ProfileSonarr.objects.create(profile_id=pid,sonarr_id=sid,lastRun='Jan 01 1970 11:59PM')
        if pk == 'delete':
            psid = int(request.POST.get('psid'))
            ps = ProfileSonarr.objects.get(id=psid)
            ps.delete()
        return Response("Ok")

class ProfileLidarrViewSet(viewsets.ModelViewSet):
    queryset = ProfileLidarr.objects.all()
    serializer_class = ProfileLidarrSerializer
    def post(self, request, pk):
        if pk == 'add':
            pid = request.POST.get('profile_id')
            lid = request.POST.get('lidarr_id')
            pl = ProfileLidarr.objects.create(profile_id=pid,lidarr_id=lid,lastRun='Jan 01 1970 11:59PM')
        if pk == 'delete':
            plid = int(request.POST.get('plid'))
            pl = ProfileLidarr.objects.get(id=plid)
            pl.delete()
        return Response("Ok")

@api_view(['GET', 'POST'])
def RunSync(request):
    #    if pk == 'execute':
    idList = request.POST.getlist('idlist[]')
    destDir = request.POST.get('destDir')
    prof_id = request.POST.get('prof_id')
    copyTheFile(idList, destDir, prof_id)
    return Response("OK")

class LogsViewSet(viewsets.ModelViewSet):
    queryset = Logs.objects.all()
    serializer_class = LogsSerializer
    def post(self, request, pk):
        if pk == 'clear':
            Logs.objects.all().delete()
        return Response("Ok")