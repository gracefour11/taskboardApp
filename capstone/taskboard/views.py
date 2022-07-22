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
        form = CreateEditTaskboardForm()
        tb_dict = retrieveTaskboardsForIndex(request)
        allTBSOwnedByMe = tb_dict['allTBSOwnedByMe']
        allTBSOwnedByOthers = tb_dict['allTBSOwnedByOthers']

        return render(request, "taskboard/index.html", {
            'form': form,
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
    allTBSOwnedByMe = Taskboard.objects.filter(user2taskboard__user=user, user2taskboard__user_role=USER_ROLE_OWNER, delete_ind=DELETE_IND_F, user2taskboard__delete_ind=DELETE_IND_F)
    allTBSOwnedByOthers = Taskboard.objects.filter(user2taskboard__user=user, user2taskboard__user_role=USER_ROLE_MEMBER, delete_ind=DELETE_IND_F, user2taskboard__delete_ind=DELETE_IND_F)

    return {
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
        form = CreateEditTaskboardForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data["taskboard_name"]
            type = form.cleaned_data["taskboard_type"]
            # deadline = form.cleaned_data["taskboard_deadline"]
            members = form.cleaned_data["taskboard_members"]
            
            # for logging purposes
            printLogForTaskboard(name, type, members)

            if (len(name) > 0 and len(type) > 0):
                # insert taskboard into db
                taskboard = Taskboard(title=name, type=type, created_by=request.user, last_modified_by=request.user)
                taskboard.save()
                print("Successfully Inserted Taskboard into DB: " + taskboard.getDict())

                # linking owner to taskboard
                owner = User.objects.get(id=request.session['_auth_user_id'])
                addUserToTaskboard(owner, taskboard, USER_ROLE_OWNER, request.user)

                # linking members to taskboard
                if (len(members) > 0): #members will be a string of "id,id,id,id"
                    print("in members list")
                    members_id_list = members.split(",")
                    for member_id in members_id_list:
                        member = User.objects.get(id=member_id)
                        addUserToTaskboard(member, taskboard, USER_ROLE_MEMBER, request.user)

                return redirect(reverse('go_to_taskboard', kwargs={ 'boardId': taskboard.id }))
            return render(request, "taskboard/index.html", {
                "form": form
            })
        return render(request, "taskboard/index.html", {
            "form": form
        })
    else:
        form = CreateEditTaskboardForm()
        return render(request, "taskboard/index.html", {
            "form": form
        })


###################################################
### FUNCTION TO EDIT TASKBOARD SETTINGS
### (only owner of taskboard is allowed to edit taskboard settings)
###################################################
@login_required
def edit_taskboard(request, boardId):
    print("in edit_taskboard")
    print(request.method)
    if (request.method == "POST"):
        form = CreateEditTaskboardForm(request.POST)
        taskboard = Taskboard.objects.get(id=boardId)
        print(form.errors)
        if form.is_valid():
            name = form.cleaned_data["taskboard_name"]
            type = form.cleaned_data["taskboard_type"]
            # deadline = form.cleaned_data["taskboard_deadline"]
            members = form.cleaned_data["taskboard_members"]

            printLogForTaskboard(name, type, members)
            
            taskboard.title = name
            taskboard.type = type
            # taskboard.deadline = deadline
            taskboard.last_modified_by = request.user
            taskboard.save()

            update_taskboard_members(request, boardId, members)
        
    return redirect(reverse('go_to_taskboard', kwargs={ 'boardId': taskboard.id }))


###################################################
### FUNCTION TO UPDATE TASKBOARD MEMBERS
###################################################
@login_required
def update_taskboard_members(request, boardId, newMembersAsStr):
    taskboard = Taskboard.objects.get(id=boardId)
    memberList_ids = User2Taskboard.objects.filter(taskboard=taskboard, user_role=USER_ROLE_MEMBER, delete_ind=DELETE_IND_F).values_list('user', flat=True)
    currMembers = User.objects.filter(id__in=memberList_ids).values_list('id', flat=True)
    currMembers_list = list(map(str, list(currMembers)))
    
    print("====== PRINT CURRENT MEMBERS LIST ===============")
    print(currMembers_list)
    newMembers_list = newMembersAsStr.split(",")
    print("====== PRINT NEW MEMBERS LIST ===============")
    print(newMembers_list)
    diff_list = getDiffBtnLists(currMembers_list, newMembers_list)
    print("====== PRINT DIFF  LIST ===============")
    print(diff_list)
    # if userId in diff_list is in currMembers, remove member
    # else: userId in diff_list is in newMembers, add member
    for userId in diff_list:
        user = User.objects.get(id=userId)
        if userId in currMembers_list:
            removeUserFromTaskboard(user, taskboard, request.user)
        else:
            addUserToTaskboard(user, taskboard, USER_ROLE_MEMBER, request.user)

###################################################
### FUNCTION TO GET TASKBOARD CONTENTS
###################################################
def get_taskboard_contents(request, boardId):
    if request.method == "GET":
        try:
            taskboard = Taskboard.objects.get(id=boardId)
            if (taskboard.type == TASKBOARD_TYPE_GRP):
                # insert member list (id and name) into serialised taskboard (if it's group)
                memberList_ids = User2Taskboard.objects.filter(taskboard=taskboard, user_role=USER_ROLE_MEMBER, delete_ind=DELETE_IND_F).values_list('user', flat=True)
                memberList_user = User.objects.filter(id__in=memberList_ids)
                print("===== memberList ======")
                print(memberList_user)
                return JsonResponse({
                    'taskboard': taskboard.serialize(),
                    'taskboard_members': [user.serialize() for user in memberList_user]
                })
            else:
                return JsonResponse({
                    'taskboard': taskboard.serialize(),
                })
        except Taskboard.DoesNotExist:
            return JsonResponse({"error": "Taskboard not found."}, status=404)


    else:
        return JsonResponse({"error": "GET request required."}, status=400)

###################################################
### FUNCTION TO DELETE TASKBOARD 
###################################################
@login_required
def delete_taskboard(request, boardId):
    taskboard = Taskboard.objects.get(id=boardId)
    user = request.user
    user2Taskboard = User2Taskboard.objects.get(user=user, taskboard=taskboard)
    if (request.method == "POST"):
        form = DeleteTaskboardForm(request.POST)
        print(form.errors)
        if form.is_valid():
            newOwner_name = form.cleaned_data["new_owner_name"]
            if (user2Taskboard.user_role == USER_ROLE_OWNER):
                # Case 1: Owned by me and Individual: Can delete
                if (taskboard.type == TASKBOARD_TYPE_IND):
                    logical_delete_taskboard(taskboard, user)
                    logical_delete_user2taskboard(taskboard, user)
                else:
                    # Case 2a: Owned by Me and Group: Leave Taskboard and assign new owner
                    if newOwner_name is not None: # delete taskboard and all associated user2taskboards
                        newOwner = User.objects.get(username=newOwner_name)
                        updateUserRoleInTaskboard(newOwner, taskboard, USER_ROLE_OWNER, user)
                        removeUserFromTaskboard(user, taskboard, user)

                    # Case 2b: Owned by Me and Group: Delete taskboard for all users
                    else: # assign new owner (don't delete taskboard)
                        logical_delete_taskboard(taskboard, user)
                        logical_delete_user2taskboards_under_taskboard(taskboard, user)
            
            # Case 3: Owned by others: Leave taskboard
            else:
                removeUserFromTaskboard(user, taskboard, user)
            
    # go back to main page
    return HttpResponseRedirect(reverse("index"))

###################################################
### FUNCTION TO GO TO TASKBOARD PAGE
###################################################
@login_required
def go_to_taskboard(request, boardId):
    taskboard = Taskboard.objects.get(id=boardId)
    sections = Section.objects.filter(taskboard=taskboard, delete_ind=DELETE_IND_F)
    user2taskboard_owner = User2Taskboard.objects.get(taskboard=taskboard, user_role=USER_ROLE_OWNER, delete_ind=DELETE_IND_F)
    isOwner = False
    if request.user.id == user2taskboard_owner.user.id:
        isOwner = True
    
    sectionForm = CreateEditSectionForm()
    taskboardForm = CreateEditTaskboardForm()
    print("current request user: " + request.user.username)
    print("taskboard owner: " + user2taskboard_owner.user.username)

    return render(request, "taskboard/taskboard.html", {
        "taskboard": taskboard,
        "sections": sections,
        "isOwner": isOwner,
        "sectionForm": sectionForm,
        "taskboardForm": taskboardForm
    })


###################################################
### FUNCTION TO CREATE SECTION
###################################################
@login_required
def create_section(request, boardId):
    if (request.method == "POST"):
        form = CreateEditSectionForm(request.POST)
        if form.is_valid():
            section_name = form.cleaned_data["section_name"]
            taskboard = Taskboard.objects.get(id=boardId)
            section = Section(name=section_name, taskboard=taskboard, created_by=request.user, last_modified_by=request.user)
            section.save()
            print("Successfully inserted Section into DB: " + section_name + " in taskboard " + taskboard.title)
    
    return redirect(reverse('go_to_taskboard', kwargs={ 'boardId': boardId}))

###################################################
### FUNCTION TO EDIT SECTION
###################################################
@login_required
def edit_section(request, boardId, sectionId):
    if (request.method == "POST"):
        form = CreateEditSectionForm(request.POST)
        if form.is_valid():
            section = Section.objects.get(id=sectionId)
            section.name = form.cleaned_data["section_name"] 
            section.last_modified_by = request.user
            section.save()
            print("Successfully updated Section into DB: " + section.name + " in taskboard " + section.taskboard.title)
    
    return redirect(reverse('go_to_taskboard', kwargs={ 'boardId': section.taskboard.id}))

###################################################
### FUNCTION TO DELETE SECTION
###################################################
@login_required
def delete_section(request, boardId, sectionId):
    section = Section.objects.get(id=sectionId)
    if (request.method == "POST"):
        form = DeleteSectionForm(request.POST)
        print(form.errors)
        print("deleting section")
        if form.is_valid():
            section.delete_ind = DELETE_IND_T
            section.last_modified_by = request.user
            section.save()
            print("Successfully deleted Section from DB: " + section.name + " from taskboard " + section.taskboard.title)
    
    return redirect(reverse('go_to_taskboard', kwargs={ 'boardId': section.taskboard.id}))