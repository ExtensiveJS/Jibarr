from MediaFileSync.models import Settings, Profile, ProfileRadarr
from rest_framework import viewsets
from rest_framework.response import Response
from .serializers import SettingsSerializer, ProfileSerializer, ProfileRadarrSerializer


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
    #def post(self, request, pk):
    def post(self, request, pk):
        if pk =='add':
            pname = request.POST.get('profile_name')
            plr = request.POST.get('profile_lastRun')
            p = Profile.objects.create(profile_name=pname,profile_lastRun=plr)
            #p.profile_name = request.POST.get('profile_name')
            #p.profile_lastRun = request.POST.get('profile_lastRun')
            #p.save()
        elif pk == 'delete':
            pid = int(request.POST.get('profile_id'))
            p = Profile.objects.get(id=pid)
            p.delete()
        return Response("Ok")

class ProfileRadarrViewSet(viewsets.ModelViewSet):
    queryset = ProfileRadarr.objects.all()
    serializer_class = ProfileRadarrSerializer
    def post(self, request, pk):
        if pk == 'add':
            pid = request.POST.get('profile_id')
            rid = request.POST.get('radarr_id')
            pr = ProfileRadarr.objects.create(profile_id=pid,radarr_id=rid,lastRun='Jan 01 1970 11:59PM')
            #pr.profile_id = request.POST.get('profile_id')
            #pr.radarr_id = request.POST.get('radarr_id')
            #pr.save()
        if pk == 'delete':
            prid = int(request.POST.get('prid'))
            pr = ProfileRadarr.objects.get(id=prid)
            pr.delete()
        return Response("Ok")