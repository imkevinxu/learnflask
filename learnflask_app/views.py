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

import os, time
import spur
import pexpect

# -----------------------------------------
#   GLOBAL VARIABLES
# -----------------------------------------

server = os.environ.get('AWS')
user = os.environ.get('AWS_USERNAME')
pem = os.environ.get('AWS_PEM')
startcode = """from flask import Flask
app = Flask(__name__)

# Your code starts here


if __name__ == "__main__":
    app.run()"""

# -----------------------------------------
#   Super janky command to add the ec2 server to the known_hosts file
#   that is associated with the django project. For some reason the normal
#   ~/.ssh/known_hosts on the heroku server allows one to ssh ONLY from a
#   python REPL + spur BUT if you try python manage.py shell + spur it can't
#   find the same known_hosts file. da fuq
# -----------------------------------------

def add_known_hosts(host, user, pem):
    child = pexpect.spawn('ssh -i %s %s@%s' % (pem, user, host))
    time.sleep(1)
    child.sendline('yes')
    child.sendline('exit')

add_known_hosts(server, user, pem)

# -----------------------------------------
#   MAIN APP FUNCTIONS
# -----------------------------------------

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

        shell = spur.SshShell(hostname=server, username=user, private_key_file=pem)
        shell.run(["sh", "-c", "echo '%s' > /var/www/flask/hello.py" % code])
        shell.run(["sh", "-c", "sudo /etc/init.d/apache2 restart"])
    else:
        code = request.session.get('code', startcode)

    return render(request, "index.html", locals())