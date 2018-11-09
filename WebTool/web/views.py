# Create your views here.
from __future__ import unicode_literals
from django.shortcuts import render_to_response


# Create your views here.
def homepage(request):
    return render_to_response('servermaterial/index.html')