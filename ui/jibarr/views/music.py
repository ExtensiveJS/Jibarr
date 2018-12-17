from django.template import loader
from django.http import HttpResponse
from jibarr.models  import Settings, Profile

def music(request):
    prof_id = 1
    try:
        prof_id = request.session["prof_id"]
    except KeyError:
        #prof_id = 1
        pass
    system_settings = Settings.objects.all()[:1].get()
    prof_list = Profile.objects.all()
    prof = Profile.objects.get(id=1)
    
    context = {
        'system_settings': system_settings,
        'system_profile': prof,
        'prof_list': prof_list,
        'prof_id': prof_id
    }
    template = loader.get_template("jibarr/music.html")
    return HttpResponse(template.render(context, request))