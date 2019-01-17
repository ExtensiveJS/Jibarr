from django.template import loader
from django.http import HttpResponse
from jibarr.models import SiteSettings, Profile
import urllib.request

def upgrade(request):
    prof_id = 1
    try:
        prof_id = request.session["prof_id"]
    except KeyError:
        pass
    system_settings = SiteSettings.objects.all()[:1].get()
    system_settings.newVersion = SiteSettings.checkVersion()

    jcv = ""
    jdv = ""
    try:
        resp = urllib.request.urlopen('https://github.com/ExtensiveJS/Jibarr/wiki/Current-Versions')
        html = resp.read()
        htmlstr = html.decode('utf8')
        htmlSplit = htmlstr.split("\n")
        for line in htmlSplit:
            if line.find('Jibarr_Code') > -1:
                jcv = line.replace("<p>","").replace("Jibarr_Code: ", "").replace("<br>","")
            if line.find('Jibarr_Database') > -1:
                jdv = line.replace("</p>","").replace("Jibarr_Database: ", "").replace("<br>","")
        resp.close()
    except:
        pass

    system_settings.jibarr_code_version = jcv
    system_settings.jibarr_database_version = jdv

    prof_list = Profile.objects.all()
    context = {
        'system_settings': system_settings,
        'prof_list': prof_list,
        'prof_id': prof_id,
    }
    template = loader.get_template("jibarr/upgrade.html")
    return HttpResponse(template.render(context, request))