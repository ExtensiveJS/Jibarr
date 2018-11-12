from MediaFileSync.models import Settings, Media
from rest_framework import serializers

class SettingsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Settings
        fields = ('id', 'radarr_enabled', 'radarr_path', 'radarr_apikey', 'sonarr_enabled', 'sonarr_path', 'lidarr_enabled', 'lidarr_path')
    #def update(self, instance, validated_data):
    #    instance.radarr_enabled = validated_data.get('radarr_enabled', instance.radarr_enabled)
    #    instance.radarr_path = validated_data.get('radarr_path', instance.radarr_path)
    #    instance.radarr_apikey = validated_data.get('radarr_apikey', insance.radarr_apikey)
    #    instance.sonarr_enabled = validated_data.get('sonarr_enabled', instance.sonarr_enabled)
    #    instance.sonarr_path = validated_data.get('sonarr_path', instance.sonarr_path)
    #    instance.lidarr_enabled = validated_data.get('lidarr_enabled', instance.lidarr_enabled)
    #    instance.lidarr_path = validated_data.get('lidarr_path', instance.lidarr_path)
    #    instance.save()
    #    return instance

class MediaSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Media
        fields = ('media_id', 'media_source', 'media_source_id', 'media_lastUpd')