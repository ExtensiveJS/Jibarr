from django.template import loader
from django.http import HttpResponse
from jibarr.models  import SiteSettings, Profile

def updates(request):
    prof_id = 1
    try:
        prof_id = request.session["prof_id"]
    except KeyError:
        pass
    system_settings = SiteSettings.objects.all()[:1].get()
    system_settings.newVersion = SiteSettings.checkVersion()
    prof_list = Profile.objects.all()
    profile_list = Profile.objects.all()
    context = {
        'system_settings': system_settings,
        'profile_list': profile_list,
        'prof_list': prof_list,
        'prof_id': prof_id
    }
    template = loader.get_template("jibarr/updates.html")
    return HttpResponse(template.render(context, request))