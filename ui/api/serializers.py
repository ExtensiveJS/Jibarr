from MediaFileSync.models import Settings, Media, Profile
from rest_framework import serializers

class SettingsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Settings
        fields = ('id', 'radarr_enabled', 'radarr_path', 'radarr_apikey', 'sonarr_enabled', 'sonarr_path', 'sonarr_apikey', 'lidarr_enabled', 'lidarr_path', 'lidarr_apikey')

class MediaSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Media
        fields = ('media_id', 'media_source', 'media_source_id', 'media_lastUpd')

class ProfileSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Profile
        fields = ('id','profile_name','profile_lastRun')