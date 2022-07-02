from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect,HttpResponseNotAllowed
from django.shortcuts import render,redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator
from django.http.response import JsonResponse
import json

from .models import *
from .forms import *
from .constants import *
from .helper import *

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
        form = CreateEditProjectForm()
        tb_dict = retrieveTaskboardsForIndex(request)
        allTBsOwnedByMeAndOthers = tb_dict['allTBsOwnedByMeAndOthers']
        allTBSOwnedByMe = tb_dict['allTBSOwnedByMe']
        allTBSOwnedByOthers = tb_dict['allTBSOwnedByOthers']

        return render(request, "taskboard/index.html", {
            'form': form,
            'allTBsOwnedByMeAndOthers': allTBsOwnedByMeAndOthers,
            'allTBSOwnedByMe': allTBSOwnedByMe,
            'allTBSOwnedByOthers': allTBSOwnedByOthers
        })
    return HttpResponseRedirect(reverse("welcome"))

###################################################
### FUNCTION TO LOAD ALL USERS THAT ARE NOT STAFF OR CURRENT REQUEST USER OR INSIDE LIST
###################################################
def load_all_users(request):
    if request.user.is_authenticated:
        print("load all users")
        all_users = User.objects.filter(is_superuser=0, is_staff=0).exclude(id=request.user.id)
        print("all_users: ")
        print(all_users)
        # return all_users
        return JsonResponse({
            'all_users': [user.serialize() for user in all_users]
        })

###################################################
### Function to retrieve all taskboards
###################################################
def retrieveTaskboardsForIndex(request):
    user = User.objects.get(id=request.session['_auth_user_id'])
    # retrieve the taskboard ids from User2Taskboard
    allTBsOwnedByMeAndOthers = Taskboard.objects.filter(user2taskboard__user=user)
    allTBSOwnedByMe = Taskboard.objects.filter(user2taskboard__user=user, user2taskboard__user_role=USER_ROLE_OWNER)
    allTBSOwnedByOthers = Taskboard.objects.filter(user2taskboard__user=user, user2taskboard__user_role=USER_ROLE_MEMBER)

    return {
        'allTBsOwnedByMeAndOthers': allTBsOwnedByMeAndOthers,
        'allTBSOwnedByMe': allTBSOwnedByMe,
        'allTBSOwnedByOthers': allTBSOwnedByOthers
    }

###################################################
### FUNCTION TO CREATE TASKBOARD
###################################################
@login_required
def create_taskboard(request):
    print("in create_taskboard")
    print(request.method)
    if (request.method == "POST"):
        form = CreateEditProjectForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data["taskboard_name"]
            type = form.cleaned_data["taskboard_type"]
            deadline = form.cleaned_data["taskboard_deadline"]
            members = form.cleaned_data["taskboard_members"]
            
            # for logging purposes
            printLogForTaskboard(name, type, deadline, members)

            if (len(name) > 0 and len(type) > 0):
                # insert taskboard into db
                taskboard = Taskboard(title=name, deadline=deadline, type=type)
                taskboard.save()
                print("Successfully Inserted Taskboard into DB: " + taskboard.getDict())

                # linking owner to taskboard
                owner = User.objects.get(id=request.session['_auth_user_id'])
                addUserToTaskboard(owner, taskboard, USER_ROLE_OWNER)

                # linking members to taskboard
                if (len(members) > 0): #members will be a string of "id,id,id,id"
                    print("in members list")
                    members_id_list = members.split(",")
                    for member_id in members_id_list:
                        member = User.objects.get(id=member_id)
                        addUserToTaskboard(member, taskboard, USER_ROLE_MEMBER)

                return redirect(reverse('go_to_taskboard', kwargs={ 'boardId': taskboard.id }))
            return render(request, "taskboard/index.html", {
                "form": form
            })
        return render(request, "taskboard/index.html", {
            "form": form
        })
    else:
        form = CreateEditProjectForm()
        return render(request, "taskboard/index.html", {
            "form": form
        })

###################################################
### FUNCTION TO ADD USER TO TASKBOARD
###################################################
def addUserToTaskboard(userId, taskboard, user_role):
    user = User.objects.get(id=userId)
    user2Taskboard = User2Taskboard(user=user, taskboard=taskboard, user_role=user_role)
    user2Taskboard.save()
    print("Successfully Inserted User2Taskboard into DB: " + user2Taskboard.getDict())


###################################################
### FUNCTION TO REMOVE USER TO TASKBOARD
###################################################
def removeUserFromTaskboard(userId, taskboard):
    user = User.objects.get(id=userId)
    user2Taskboard = User2Taskboard.objects.get(user=user, taskboard=taskboard)
    user2Taskboard.user_role = USER_ROLE_REMOVED
    user2Taskboard.save()
    print("Successfully Removed User2Taskboard: " + user2Taskboard.getDict())


###################################################
### FUNCTION TO UPDATE USER ROLE IN TASKBOARD
###################################################
def updateUserRoleInTaskboard(user, taskboard, user_role):
    user2Taskboard = User2Taskboard.objects.get(user=user, taskboard=taskboard)
    user2Taskboard.user_role = user_role
    user2Taskboard.save()
    print("Successfully Removed User2Taskboard: " + user2Taskboard.getDict())

###################################################
### FUNCTION TO EDIT TASKBOARD SETTINGS
### (only owner of taskboard is allowed to edit taskboard settings)
###################################################
@login_required
def edit_taskboard(request, boardId):
    print("in edit_taskboard")
    print(request.method)
    if (request.method == "POST"):
        form = CreateEditProjectForm(request.POST)
        taskboard = Taskboard.objects.get(id=boardId)
        if form.is_valid():
            name = form.cleaned_data["taskboard_name"]
            type = form.cleaned_data["taskboard_type"]
            deadline = form.cleaned_data["taskboard_deadline"]
            members = form.cleaned_data["taskboard_members"]

            printLogForTaskboard(name, type, deadline, members)
            
            taskboard.name = name
            taskboard.type = type
            taskboard.deadline = deadline
            taskboard.save()

            update_taskboard_members(boardId, members)


###################################################
### FUNCTION TO UPDATE TASKBOARD MEMBERS
###################################################
@login_required
def update_taskboard_members(boardId, newMembersAsStr):
    taskboard = Taskboard.objects.get(id=boardId)
    
    # get list of current members' ids
    currMembers = User.objects.filter(user2taskboard__taskboard=taskboard, user2taskboard__user_role=USER_ROLE_MEMBER).values_list('id', flat=True)
    currMembers_list = list(currMembers)

    # get list of new members' ids
    newMembers_list = newMembersAsStr.split(",")

    # find differences between the 2 lists
    diff_list = getDiffBtnLists(currMembers_list, newMembers_list)

    # if userId in diff_list is in currMembers, remove member
    # else: userId in diff_list is in newMembers, add member
    for userId in diff_list:
        if userId in currMembers_list:
            removeUserFromTaskboard(userId, taskboard)
        else:
            addUserToTaskboard(userId, taskboard)




###################################################
### FUNCTION TO DELETE TASKBOARD 
###################################################
# - Owned by me and Individual: Can delete
# - Owned by me and Group: Can delete but need to assign new owner
# - Owned by others: Cannot delete but have option: Leave Taskboard.
@login_required
def delete_taskboard(request, boardId):
    taskboard = Taskboard.objects.get(id=boardId)
    user = request.user
    user2Taskboard = User2Taskboard.objects.get(user=user, taskboard=taskboard)

    if (user2Taskboard.user_role == USER_ROLE_OWNER):
        if (taskboard.type == TASKBOARD_TYPE_IND):
            pass
    pass

###################################################
### FUNCTION TO LEAVE TASKBOARD 
###################################################
@login_required
def leave_taskboard(request, boardId):
    pass

###################################################
### FUNCTION TO GO TO TASKBOARD PAGE
###################################################
@login_required
def go_to_taskboard(request, boardId):
    return render(request, "taskboard/taskboard.html", {
        "boardId": boardId
    })



