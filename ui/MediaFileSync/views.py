import time
from time import mktime
from datetime import datetime
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
import MediaFileSync.checkFolder
from .models import Media
from .models2 import Movies


def syncprocessor(request):
    #runSimulate = True
    #strPage = "...processing started @ " + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "<br />"
    #lastRun = "Mar 29 1971 6:07PM"
    #strPage = MediaFileSync.checkFolder.checkFolder("d:/videos/","d:/temp/", datetime.fromtimestamp(mktime(time.strptime(lastRun, "%b %d %Y %I:%M%p"))), strPage, runSimulate)
    #strPage += "...processing ended @ " + datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    #return HttpResponse(strPage)
    context = {}
    template = loader.get_template("MediaFileSync/index.html")
    return HttpResponse(template.render(context, request))

def simulated(request):
    context = {}
    template = loader.get_template("MediaFileSync/simulated.html")
    return HttpResponse(template.render(context, request))

def runsimulated(request):
    return HttpResponseRedirect("http://google.com")

def index(request):
    media_list = Media.objects.all() #.objects.order_by(id)
    radarr_list = Movies.objects.using("radarr").all()
   
    strPage = "<html><body style='background-color:black;'>"
    strPage += "<div style='position:relative;'>"

    # HEADER MENU
    strPage += "<div style='margin:50px 150px auto 150px;height:100px;color:white;'>"
    strPage += "<div style='width:100px;text-align:center;float:left;'>HOME</div>"
    strPage += "<div style='width:100px;text-align:center;float:left;'>LIST</div>"
    strPage += "<div style='width:100px;text-align:center;float:left;'>PROFILES</div>"
    strPage += "<div style='width:100px;text-align:center;float:left;'>SETTINGS</div>"
    strPage += "</div>"

    strPage += "<div style='background-color:whitesmoke;margin:20px 150px auto 150px;color:black;padding:5px;'>"
    strPage += "<table style='width:100%;'><thead><tr><th style='text-align:left;'>id</th>"
    strPage += "<th style='text-align:left;'>source</th>"
    strPage += "<th style='text-align:left;'>lastUpd</th></tr></thead><tbody>"
    for val in media_list:
    #    #strPage += val
    #    ms = Media.objects.get(id=1).media_source
        strPage += "<tr><td>" + str(val.media_id) + "</td>"
        strPage += "<td>" + val.media_source + "</td>"
        strPage += "<td>" + val.media_lastUpd.strftime("%Y-%m-%d %H:%M:%S") + "</td></tr>"
    strPage += "</tbody></table>"
    strPage += "</div>"

    strPage += "<div style='background-color:whitesmoke;margin:20px 150px auto 150px;color:black;padding:5px;'>"
    strPage += "<table style='width:100%;'><thead><tr><th style='text-align:left;'>id</th>"
    strPage += "<th style='text-align:left;'>title</th>"
    strPage += "<th style='text-align:left;'>lastUpd</th></tr></thead><tbody>"
    for val in radarr_list:
    #    #strPage += val
    #    ms = Media.objects.get(id=1).media_source
        strPage += "<tr><td>" + str(val.id) + "</td>"
        strPage += "<td>" + val.title + "</td>"
        strPage += "<td>" + val.lastinfosync.strftime("%Y-%m-%d %H:%M:%S") + "</td></tr>"
    strPage += "</tbody></table>"
    strPage += "</div>"

    strPage += "</div>"
    strPage += "</body></html>"
    return HttpResponse(strPage)