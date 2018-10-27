import datetime
from django.db import models
from django.utils import timezone

# Create your models here.

class Media(models.Model):
    media_id = models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    media_source = models.CharField(max_length=200)
    media_source_id = models.IntegerField()
    media_lastUpd = models.DateTimeField()
    #def __str__(self):
    #    return self.question_text
    def was_updated_recently(self):
        return self.media_lastUpd >= timezone.now() - datetime.timedelta(days=1)

class Profile(models.Model):
    profile_id = models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    profile_name = models.CharField(max_length=200)
    profile_lastUpd = models.DateTimeField()
    
class ProfileMedia(models.Model):
    profilemedia_id = models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    profile_id = models.IntegerField()
    media_id = models.IntegerField()

class Settings(models.Model):
    id = models.IntegerField(db_column='Id', auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    radarr_enabled = models.IntegerField(db_column='RADARR_Enabled', null=False)
    radarr_path =  models.TextField(db_column='RADARR_Path')
    sonarr_enabled = models.IntegerField(db_column='SONARR_Enabled', null=False)
    sonarr_path =  models.TextField(db_column='SONARR_Path')
    lidarr_enabled = models.IntegerField(db_column='LIDARR_Enabled', null=False)
    lidarr_path =  models.TextField(db_column='LIDARR_Path')
    class Meta:
        managed = False
        db_table = 'MediaFileSync_settings'