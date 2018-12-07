# Create your views here.
from __future__ import unicode_literals
from django.shortcuts import render_to_response


# Create your views here.
def homepage(request):
    return render_to_response('servermaterial/index.html')

def monitor_all(request):
    return render_to_response('servermaterial/monitor_all.html')

def study_well(request):
    return render_to_response('servermaterial/study_well.html')

def study_poor(request):
    return render_to_response('servermaterial/study_poor.html')

def first(request):
    return render_to_response('servermaterial/first.html')
