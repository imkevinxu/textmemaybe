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
        user = authenticate(username=request.POST['email'], password=request.POST['password'])
        if user is not None:
            if user.is_active:
                login(request, user)
                # Redirect to a success page.
                return redirect('profile')
            else:
                # Return a 'disabled account' error message
                pass
        else:
            # Return an 'invalid login' error message.
            pass

    return redirect('index')

def profile(request):

    try:
        number = Number.objects.get(user=request.user)
        friendly_number = '('+str(number.number)[1:4]+') '+str(number.number)[4:7]+'-'+str(number.number)[7:11]
        messages = twilio_client.sms.messages.list(to=str(number.number)[:11])

        # messages = twilio_client.sms.messages.list(to="6503534542")
        for i, m in enumerate(messages):
            from_number = float(m.from_[2:])
            try:
                signup = Signup.objects.get(number=float(from_number), group_number=float(number.number))
                pass
            except:
                friendly_from_number = '('+str(from_number)[:3]+') '+str(from_number)[3:6]+'-'+str(from_number)[6:10]
                body = m.body.split()
                email = ''
                for b in body:
                    if "," in b:
                        b.remove(',')
                    if "@" in b:
                        email = b
                        body.remove(b)
                name = " ".join(body)
                #time sent is off
                signup = Signup(user=request.user, number = from_number, friendly_from_number=friendly_from_number, name=name, email=email, group_name=number.name, group_number=number.number)
                signup.save()


        messages = Signup.objects.filter(user=request.user)
    except:
        pass

    return render(request, "profile.html", locals())

def create(request):
    if request.POST.get('name') and request.POST.get('message'):
        numbers = twilio_client.phone_numbers.search(area_code=650)
        if numbers:
            numbers[0].purchase()

            n = Number(user=request.user, number=numbers[0].phone_number, name=request.POST['name'], message=request.POST['message'])
            n.save()

            # path = default_storage.save(os.path.join(settings.MEDIA_ROOT,'sms',n.number[1:]), ContentFile('<Response><Sms>'+n.message+'</Sms></Response>'))
            # sms_url = "http://textmemaybe.co/media/sms/" + n.number[1:]
            sms_url = 'http://twimlets.com/echo?Twiml=%3CResponse%3E%3CSms%3E'+n.message.replace(' ', '%20')+'%3C%2FSms%3E%3C%2FResponse%3E'
            n.sms_url = sms_url
            n.save()

            for number in twilio_client.phone_numbers.list(api_version="2010-04-01"):
                if number.phone_number == n.number:
                    number.update(SmsUrl=sms_url, SmsFallbackUrl='http://twimlets.com/echo?Twiml=%3CResponse%3E%3CSms%3EThanks%20for%20signing%20up%3C%2FSms%3E%3C%2FResponse%3E')
                    break

        else:
            error = "No numbers in 650 available"
            print error


    return redirect('profile')