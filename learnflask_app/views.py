from django import forms
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core import serializers
from django.core.context_processors import csrf
from django.core.mail import send_mail
from django.http import HttpResponse, HttpResponseRedirect
from coffin.shortcuts import render_to_response, get_object_or_404, render, \
    redirect
from django.template import loader, RequestContext
from django.views.decorators.csrf import csrf_exempt

from learnflask_app.models import *
from learnflask_app.model_forms import *
from learnflask_app.forms import *

import os
import spur

startcode = """from flask import Flask
app = Flask(__name__)

# Your code starts here


if __name__ == "__main__":
    app.run()"""

def index(request):
    step = 1
    code = startcode
    return render(request, "index.html", locals())

def route(request):
    step = 2
    if request.method == "POST":
        code = request.POST['code']
        request.session['code'] = code
    else:
        code = request.session.get('code', startcode)
    return render(request, "index.html", locals())

def hello(request):
    step = 3
    if request.method == "POST":
        code = request.POST['code']
        request.session['code'] = code
    else:
        code = request.session.get('code', startcode)
    return render(request, "index.html", locals())

def deploy(request):
    step = 4
    if request.method == "POST":
        code = request.POST['code']
        request.session['code'] = code
    else:
        code = request.session.get('code', startcode)
    return render(request, "index.html", locals())

def deployed(request):
    step = 5
    server = os.environ.get('AWS')
    if request.method == "POST":
        code = request.POST['code']
        request.session['code'] = code
        username = os.environ.get('AWS_USERNAME')
        pem = os.environ.get('AWS_PEM')

        shell = spur.SshShell(hostname=server, username=username, private_key_file=pem)
        shell.run(["sh", "-c", "echo '%s' > /var/www/flask/hello.py" % code])
        shell.run(["sh", "-c", "sudo /etc/init.d/apache2 restart"])
    else:
        code = request.session.get('code', startcode)

    return render(request, "index.html", locals())