from django.template import loader
from django.http import HttpResponse
from jibarr.models  import Settings, Profile, Logs

def logs(request):
    prof_id = 1
    try:
        prof_id = request.session["prof_id"]
    except KeyError:
        pass
    system_settings = Settings.objects.all()[:1].get()
    prof_list = Profile.objects.all()
    log_list = Logs.objects.all()
    context = {
        'system_settings': system_settings,
        'log_list': log_list,
        'prof_list': prof_list,
        'prof_id': prof_id
    }
    template = loader.get_template("jibarr/logs.html")
    return HttpResponse(template.render(context, request))