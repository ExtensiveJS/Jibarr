from MediaFileSync.models import Settings
from rest_framework import viewsets
from rest_framework.response import Response
from .serializers import SettingsSerializer


class SSSettingsViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Settings to be viewed or edited.
    """
    queryset = Settings.objects.all()
    serializer_class = SettingsSerializer

class SettingsViewSet(viewsets.ModelViewSet):
    queryset = Settings.objects.all()
    serializer_class = SettingsSerializer
    def post(self, request, pk):
        sett = Settings.objects.all()[:1].get()
        
        sett.radarr_enabled = request.POST.get('radarr_enabled')
        sett.radarr_path = request.POST.get('radarr_path')
        sett.sonarr_enabled = request.POST.get('sonarr_enabled')
        sett.sonarr_path = request.POST.get('sonarr_path')
        sett.lidarr_enabled = request.POST.get('lidarr_enabled')
        sett.lidarr_path = request.POST.get('lidarr_path')


        sett.save()
        return Response("Ok")