from django.shortcuts import render

import datetime
import time
import json

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.template import RequestContext, Context, Template
from django.core.mail import send_mail
from django.core.urlresolvers import reverse

from django.conf import settings

def index(request):
    return render_to_response('index.html', 
                              {},
                              context_instance=RequestContext(request))

def about(request):
    return render_to_response('about.html', 
                              {},
                              context_instance=RequestContext(request))

def projects(request):
    return render_to_response('projects.html', 
                              {},
                              context_instance=RequestContext(request))