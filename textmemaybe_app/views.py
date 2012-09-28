from django import forms
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core import serializers
from django.core.context_processors import csrf
from django.core.mail import send_mail
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404, render, \
    redirect
from django.template import loader, RequestContext
from django.views.decorators.csrf import csrf_exempt

from textmemaybe_app.models import *
from textmemaybe_app.model_forms import *
from textmemaybe_app.forms import *

from django.conf import settings
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django_twilio.client import twilio_client

#@login_required
def index(request):
    if request.user.is_authenticated():
        return redirect('profile')


    # # numbers = twilio.phone_numbers.search(area_code=646)
    # # if numbers:
    # #     numbers[0].purchase()
    # # else:
    # #     print "No numbers available"

    # if request.user.username == "purplelover":
    #     messages = twilio.sms.messages.list(to="6464900572")
    #     for i, m in enumerate(messages):
    #         body = m.body.split()
    #         m.email = body[len(body)-1]
    #         m.name = " ".join(body[:len(body)-1])
    #         messages[i] = m


    #     messages2 = twilio.sms.messages.list(to="6464806507")
    #     for i, m in enumerate(messages2):
    #         body = m.body.split()
    #         m.email = body[len(body)-1]
    #         m.name = " ".join(body[:len(body)-1])
    #         messages2[i] = m

    return render(request, "index.html", locals())

def register(request):

    if request.POST.get('email') and request.POST.get('password'):
        user = User.objects.create_user(request.POST['email'], request.POST['email'], request.POST['password'])
        user.save()
        return redirect('profile')

    return redirect('index')

def profile(request):

    return render(request, "profile.html", locals())

def create(request):
    if request.POST.get('name') and request.POST.get('message'):
        numbers = twilio_client.phone_numbers.search(area_code=650)
        if numbers:
            # numbers[0].purchase()

            # n = Number(user=request.user, number=numbers[0].phone_number, name=request.POST['name'], message=request.POST['message'])
            # n.save()

            # path = default_storage.save('sms/'+n.number[1:], ContentFile('<Response><Sms>'+n.message+'</Sms></Response>'))
            path = default_storage.save(os.path.join(settings.MEDIA_ROOT,'sms','hahaha'), ContentFile('<Response><Sms>Woah</Sms></Response>'))
            print path
            # sms_url = "http://textmemaybe.co/media/sms/" + n.number[1:]
            # n.sms_url = sms_url
            # n.save()

            # numbers[0].update(SmsUrl=sms_url)

        else:
            error = "No numbers in 650 available"
            print error


    return redirect('profile')