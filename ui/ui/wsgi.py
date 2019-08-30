"""
WSGI config for ui project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/howto/deployment/wsgi/
"""

import os, json
from jibarr.models import SiteSettings, Logs
from urllib.request import urlopen
from django.core.wsgi import get_wsgi_application
from django.conf import settings
from datetime import datetime
from jibarr import SystemUpgrade

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ui.settings')

application = get_wsgi_application()

settings.isConnected = False
settings.isSonarrConnected = False
settings.isRadarrConnected = False
system_settings = SiteSettings.objects.all()[:1].get()

# get db version
dbVer = system_settings.jibarr_version
# get settings version
appVer = settings.CODE_VERSION
# compare
if dbVer != appVer:
    # backup DB
    try:
        SystemUpgrade.backupDatabase()
    except Exception as e:
        pass
    # run update
    try:
        SystemUpgrade.upgradeDatabase(dbVer,appVer)
    except Exception as e:
        pass

try:
    data = urlopen(system_settings.radarr_path + "/api/system/status/?apikey=" + system_settings.radarr_apikey).read()
    json.loads(data)
    settings.isConnected = True
    settings.isRadarrConnected = True
except:
    pass

try:
    data2 = urlopen(system_settings.sonarr_path + "/api/system/status/?apikey=" + system_settings.sonarr_apikey).read()
    json.loads(data2)
    settings.isSonarrConnected = True
except:
    pass

try:
    Logs.objects.create(log_type='System',log_category='System',log_message='Jibarr system started.',log_datetime=datetime.utcnow().strftime("%b %d %Y %H:%M:%S"))
except KeyError:
    pass