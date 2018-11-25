from MediaFileSync.models import Settings, Profile, ProfileSonarr, sonarrShow, sonarrShowList
from urllib.request import urlopen
import json
from time import mktime
from datetime import datetime
import time
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader

def shows(request):
    prof_id = 1
    try:
        prof_id = request.session["prof_id"]
    except KeyError:
        pass
    system_settings = Settings.objects.all()[:1].get()
    prof_list = Profile.objects.all()
    prof = Profile.objects.get(id=prof_id)
    
    context = {
        'system_settings': system_settings,
        'system_profile': prof,
        'show_list': get_show_info(system_settings, prof),
        'prof_list': prof_list,
        'prof_id': prof_id
    }
    template = loader.get_template("MediaFileSync/shows.html")
    return HttpResponse(template.render(context, request))

def get_show_info(system_settings, prof):
    sSL = sonarrShowList()
    sSL.showlist.clear
    psList = ProfileSonarr.objects.filter(profile_id=prof.id)
    data = urlopen(system_settings.sonarr_path + "/api/series?apikey=" + system_settings.sonarr_apikey).read()
    output = json.loads(data)

    return sSL