from MediaFileSync.models import Settings
from rest_framework import serializers

class SettingsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Settings
        fields = ('id', 'radarr_enabled', 'radarr_path', 'sonarr_enabled', 'sonarr_path', 'lidarr_enabled', 'lidarr_path')