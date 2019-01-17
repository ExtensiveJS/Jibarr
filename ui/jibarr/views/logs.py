from django.template import loader
from django.http import HttpResponse
from jibarr.models  import SiteSettings, Profile, Logs

def logs(request):
    prof_id = 1
    try:
        prof_id = request.session["prof_id"]
    except KeyError:
        pass
    filterCriteria = "all"
    try:
        if(request.GET.get("filter")):
            if(request.GET.get("filter") == "Media"):
                filterCriteria = "Radarr"
            else:
                filterCriteria = request.GET.get("filter")
    except KeyError:
        pass
    system_settings = SiteSettings.objects.all()[:1].get()
    system_settings.newVersion = SiteSettings.checkVersion()
    prof_list = Profile.objects.all()
    if(filterCriteria=='all'):
        log_list = Logs.objects.all().order_by('-log_datetime')
    else:
        log_list = Logs.objects.all().order_by('-log_datetime').filter(log_category = filterCriteria)


    context = {
        'system_settings': system_settings,
        'log_list': log_list,
        'prof_list': prof_list,
        'prof_id': prof_id
    }
    template = loader.get_template("jibarr/logs.html")
    return HttpResponse(template.render(context, request))