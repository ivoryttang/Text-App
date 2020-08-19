from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from textapp.models import Channel, Message
import logging
from django import forms

#create views here.
def index(request):
    if not request.user.is_authenticated:
        return render(request, "login.html", {"message": None})
    context = {
        "user": request.user,
        "channels": Channel.objects.all()
    }

    return render(request, "user.html", context)

def create_channel(request):
    name = request.POST["new_channel"]
    c = Channel(name=name)
    c.save()
    context = {
        "user": request.user,
        "channels": Channel.objects.all()
    }
    return render(request, "user.html", context)

def create_message(request):
    #if request.method == "POST":
        #form = PostForm(request.POST)
        #if form.is_valid():
        # do processing
        # save model, etc.
            #return HttpResponseRedirect("newm/")
    content = request.POST["new_message"]
    channel = Channel.objects.first()
    m = Message(content=content, channel=channel, user=request.user)
    m.save()
    context = {
        "user": request.user,
        "channels": Channel.objects.all(),
        "messages": Message.objects.filter(channel_id=channel.id)
    }
    #return render_to_response("user.html", context, context_instance=RequestContext(request))

    return render(request, "user.html", context)

def get_messages_for_channel(request):
    channel = Channel.objects.all().filter(name=request.POST["selected_channel"])[0]
    new_message = Message()
    new_message.content="hi"
    new_message.channel=channel
    new_message.save()
    messages = Message.objects.filter(channel_id=channel.id)
    context = {
        "user": request.user,
        "channels": Channel.objects.all(),
        "messages": messages
    }
    return render(request, "user.html", context)

def login_view(request):
    username = request.POST.get('username', False)
    password = request.POST.get("password",False)
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "login.html", {"message": "Invalid credentials."})

def logout_view(request):
    logout(request)
    return render(request, "login.html", {"message": "Logged out."})