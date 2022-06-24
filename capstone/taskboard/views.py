from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect,HttpResponseNotAllowed
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator
from django.http.response import JsonResponse
import json
from django.core import serializers
from .models import *
from . import forms


###################################################
### LOGIN CURRENT USER
###################################################
def login_view(request):
    if request.method == "POST":
        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return HttpResponseRedirect(reverse("welcome"))
    else:
        return render(request, "taskboard/welcome.html")

###################################################
### LOGOUT CURRENT USER
###################################################
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("welcome"))

###################################################
### REGISTER CURRENT USER AS NEW USER
###################################################
def register(request):
    if request.method == "POST":
        username = request.POST["reg_username"]
        email = request.POST["reg_email"]

        # Ensure password matches confirmation
        password = request.POST["reg_password"]
        confirmation = request.POST["reg_confirmation"]
        if password != confirmation:
            return render(request, "taskboard/welcome.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "taskboard/welcome.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "taskboard/welcome.html")

###################################################
### WELCOME PAGE
###################################################
def welcome(request):
    if request.method == "POST":
        return HttpResponseNotAllowed(["GET"])
    return render(request, "taskboard/welcome.html")

###################################################
### HOME PAGE
###################################################
def index(request):
    if request.user.is_authenticated:
        all_users = load_all_users(request)
        form = forms.CreateEditProjectForm()
        return render(request, "taskboard/index.html", {
            'all_users': all_users,
            'form': form
        })
    return HttpResponseRedirect(reverse("welcome"))

###################################################
### FUNCTION TO LOAD ALL USERS THAT ARE NOT STAFF OR CURRENT REQUEST USER
###################################################
def load_all_users(request):
    if request.user.is_authenticated:
        print("load all users")
        all_users = User.objects.filter(is_superuser=0, is_staff=0).exclude(id=request.user.id)
        print(all_users)
        return all_users

###################################################
### MY TASKBOARDS PAGE
###################################################
def taskboards_view(request):
    # TODO for view my taskboards page
    return render(request, "taskboard/myTaskboards.html")

###################################################
### FUNCTION TO CREATE TASKBOARD
###################################################
@login_required
def create_taskboard(request):
    print("in create_taskboard")
    print(request.method)
    if (request.method == "POST"):
        form = forms.CreateEditProjectForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data["taskboard_name"]
            type = form.cleaned_data["taskboard_type"]
            deadline = form.cleaned_data["taskboard_deadline"]
            members = form.cleaned_data["taskboard_members"]
            
            # for logging purposes
            print("Created Taskboard: " + name)
            print("New taskboard type: "+ type)
            if (deadline is not None):
                print("New taskboard deadline: " + deadline.strftime('%Y-%m-%d'))
            else:
                print("New taskboard deadline: ")
            print("New taskboard members list: " + members)

            if (len(name) > 0 and len(type) > 0):
                # insert taskboard into db
                taskboard = Taskboard(title=name, deadline=deadline, type=type)
                taskboard.save()
                print("Successfully Inserted Taskboard into DB: " + taskboard.getDict())

                # linking owner to taskboard
                owner = User.objects.get(id=request.session['_auth_user_id'])
                user2Taskboard_forOwner = User2Taskboard(user=owner, taskboard=taskboard, user_role="OWNER")
                user2Taskboard_forOwner.save()
                print("Successfully Inserted User2Taskboard (for owner) into DB: " + user2Taskboard_forOwner.getDict())

                # linking members to taskboard
                if (len(members) > 0): #members will be a string of "id,id,id,id"
                    print("in members list")
                    members_id_list = members.split(",")
                    for member_id in members_id_list:
                        member = User.objects.get(id=member_id)
                        user2Taskboard_forMember = User2Taskboard(user=member, taskboard=taskboard, user_role="MEMBER")
                        user2Taskboard_forMember.save()
                        print("Successfully Inserted User2Taskboard (for member) into DB: " + user2Taskboard_forMember.getDict())

                return render(request, "taskboard/taskboard.html")
            return render(request, "taskboard/index.html", {
                "form": form
            })
        return render(request, "taskboard/index.html", {
            "form": form
        })
    else:
        form = forms.CreateEditProjectForm()
        return render(request, "taskboard/index.html", {
            "form": form
        })
