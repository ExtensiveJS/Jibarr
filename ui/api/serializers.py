from MediaFileSync.models import Settings
from rest_framework import serializers

class SettingsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Settings
        fields = ('id', 'radarr_enabled', 'radarr_path', 'sonarr_enabled', 'sonarr_path', 'lidarr_enabled', 'lidarr_path')
    def update(self, instance, validated_data):
        instance.radarr_enabled = validated_data.get('radarr_enabled', instance.radarr_enabled)
        instance.radarr_path = validated_data.get('radarr_path', instance.radarr_path)
        instance.sonarr_enabled = validated_data.get('sonarr_enabled', instance.sonarr_enabled)
        instance.sonarr_path = validated_data.get('sonarr_path', instance.sonarr_path)
        instance.lidarr_enabled = validated_data.get('lidarr_enabled', instance.lidarr_enabled)
        instance.lidarr_path = validated_data.get('lidarr_path', instance.lidarr_path)
        instance.save()
        return instance
    #def updatepath(newpath):
    #    return newpath
