from MediaFileSync.models import Settings
from rest_framework import viewsets
from .serializers import SettingsSerializer


class SettingsViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Settings to be viewed or edited.
    """
    queryset = Settings.objects.all()
    serializer_class = SettingsSerializer