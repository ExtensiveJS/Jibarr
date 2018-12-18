from jibarr.models import Settings, Profile, ProfileRadarr, ProfileSonarr, ProfileLidarr, Logs
from rest_framework import serializers

class SettingsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Settings
        fields = ('id', 'radarr_enabled', 'radarr_path', 'radarr_apikey', 'sonarr_enabled', 'sonarr_path', 'sonarr_apikey', 'lidarr_enabled', 'lidarr_path', 'lidarr_apikey')

class ProfileSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Profile
        fields = ('id','profile_name','profile_lastRun')

class ProfileRadarrSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ProfileRadarr
        fields = ('id', 'profile_id', 'radarr_id', 'lastRun')

class ProfileSonarrSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ProfileSonarr
        fields = ('id', 'profile_id', 'sonarr_id', 'lastRun')

class ProfileLidarrSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ProfileLidarr
        fields = ('id', 'profile_id', 'lidarr_id', 'lastRun')

class LogsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Logs
        fields = ('id','log_type','log_message','log_category','log_datetime')