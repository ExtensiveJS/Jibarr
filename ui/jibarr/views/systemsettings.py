import os
from django.template import loader
from django.http import HttpResponse
from os import listdir
from os.path import isfile, join, dirname, abspath
from jibarr.models import SiteSettings, Profile

def systemsettings(request):
    prof_id = 1
    try:
        prof_id = request.session["prof_id"]
    except KeyError:
        #prof_id = 1
        pass
    system_settings = SiteSettings.objects.all()[:1].get()
    system_settings.newVersion = SiteSettings.checkVersion()
    prof_list = Profile.objects.all()
    context = {
        'system_settings': system_settings,
        'prof_list': prof_list,
        'prof_id': prof_id,
        'backupList': get_backup_list(),
        'backupLocation': abspath(dirname(dirname(abspath(__file__))) + "\\..\\backup\\")
    }
    template = loader.get_template("jibarr/systemsettings.html")
    return HttpResponse(template.render(context, request))

def get_backup_list():
    mypath = dirname(dirname(abspath(__file__))) + "\\..\\backup\\"
    # "d:\\sandbox\\jibarr\\ui\\backup\\"
    # onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
    #onlyfiles = os.listdir(mypath)
    onlyfiles = []
    for f in os.listdir(mypath):
        if f.endswith("bak"): # to avoid other files
            onlyfiles.append(f) # modify the concatenation to fit your neet

    return onlyfiles