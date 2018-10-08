import datetime
from django.db import models
from django.utils import timezone

# Create your models here.

class Media(models.Model):
    media_id = models.IntegerField()
    media_source = models.CharField(max_length=200)
    media_source_id = models.IntegerField()
    media_lastUpd = models.DateTimeField()
    #def __str__(self):
    #    return self.question_text
    def was_updated_recently(self):
        return self.media_lastUpd >= timezone.now() - datetime.timedelta(days=1)