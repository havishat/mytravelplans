# -*- coding: utf-8 -*-
from __future__ import unicode_literals
# Create your views here.
from django.shortcuts import render, HttpResponse, redirect
from models import *
from django.contrib import messages
import datetime
today=str(datetime.date.today())

# the index function is called when root is visited
def index(request):
    return render(request,"beltexam/index.html")

def register(request):
    result = User.objects.validate_registration(request.POST)
    if type(result) == list:
        for err in result:
            messages.error(request, err)
        return redirect('/')
    # user = User.objects.create(password=request.POST['password'],username=request.POST['username'],name=request.POST['name'])
    request.session['user_id'] = result.id
    return redirect('/travel')

def login(request):
    result = User.objects.validate_login(request.POST)
    if type(result) == list:
        for err in result:
            messages.error(request, err)
        return redirect('/')
    # user = User.objects.get(username=request.POST['username'])
    request.session['user_id'] = result.id
    return redirect('/travel')

def travel(request):
    print request.session['user_id']
    try:
        request.session['user_id']
    except KeyError:
        return redirect('/')
    context = {
        # 'destination': User.objects.get(id=request.session['user_id']).added_destination.all(),
        'destination': Destination.objects.filter(join_by=User.objects.get(id=request.session['user_id'])),

        'user': User.objects.get(id=request.session['user_id']),
        'all_destination': Destination.objects.exclude(join_by=User.objects.get(id=request.session['user_id']))
    }

    return render(request,"beltexam/success.html", context)

def addtravelplan(request):
    startdate = request.POST['startdate']
    enddate = request.POST['enddate']
    if len(request.POST['destination']) == 0 | len(request.POST['description']) == 0 :
        messages.error(request, "Entry should not be empty")
        return redirect("/travel_plan/add")
    elif startdate <= today :
        messages.error(request, "Date should be from future")
        return redirect("/travel_plan/add")
    elif startdate >= enddate :
        messages.error(request, "Travel date should be before the travel date from")
        return redirect("/travel_plan/add")
    else:
        Destination.objects.create(destination=request.POST['destination'], description=request.POST['description'],startdate=request.POST['startdate'],enddate=request.POST['enddate'],added = User.objects.get(id = request.session['user_id']))
        User.objects.get(id = request.session['user_id']).join_destination.add(Destination.objects.get(destination=request.POST['destination'], description=request.POST['description'],startdate=request.POST['startdate'],enddate=request.POST['enddate']))
        return redirect('/travel')

def join(request, id):
    Destination.objects.get(id=id).join_by.add(User.objects.get(id=request.session['user_id']))
    return redirect('/travel')


def create(request):
    return render(request,"beltexam/traveladd.html")


def plans(request,id):
    try:
        request.session['user_id']
    except KeyError:
        return redirect('/')
    context = {
        'destination': Destination.objects.get(id=id),
        # 'users_added': Destination.objects.exclude(join_by__username=2, id=id)
        'users_added': User.objects.filter(join_destination__id=id).exclude(added_destination__id=id)
        
    }
    # print Destination.objects.exclude(join_destination__id=id).filter(id=id).values() , "eh"
    return render(request,"beltexam/plan.html", context)


def logout(request):
	request.session['user'] = None
	return redirect("/")

def delete(request, id):
    Destination.objects.get(id=id).delete()
    return redirect("/travel")

def remove(request, id):
    Destination.objects.get(id=id).join_by.remove(User.objects.get(id = request.session['user_id']))
    return redirect("/travel")