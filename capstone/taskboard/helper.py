from .models import *
from .forms import *
from .constants import *
import re

##########################################################
## Returns a list containing difference between 2 lists
##########################################################
def getDiffBtnLists(li1, li2):
    return list(set(li1) - set(li2)) + list(set(li2) - set(li1))

##########################################################
## Print log for taskboard
##########################################################
def printLogForTaskboard(name, type, members):
    print("Taskboard: " + name)
    print("New taskboard type: "+ type)
    print("New taskboard members list: " + members)


###################################################
### FUNCTION TO LOGICALLY DELETE TASKBOARD
###################################################
def logical_delete_taskboard(taskboard, request_user):
    taskboard.delete_ind = DELETE_IND_T
    taskboard.last_modified_by = request_user
    taskboard.save()

###################################################
### FUNCTION TO LOGICALLY DELETE ALL USER2TASKBOARDS UNDER TASKBOARD
###################################################
def logical_delete_user2taskboards_under_taskboard(taskboard, request_user):
    User2Taskboard.filter(taskboard=taskboard, delete_ind=DELETE_IND_F).update(delete_ind=DELETE_IND_T, last_modified_by=request_user)

###################################################
### FUNCTION TO LOGICALLY DELETE USER2TASKBOARD
###################################################
def logical_delete_user2taskboard(user2taskboard, request_user):
    user2taskboard.delete_ind = DELETE_IND_T
    user2taskboard.last_modified_by = request_user
    user2taskboard.save()


###################################################
### FUNCTION TO ADD USER TO TASKBOARD
###################################################
def addUserToTaskboard(user, taskboard, user_role, request_user):
    user2Taskboard = User2Taskboard(user=user, taskboard=taskboard, user_role=user_role)
    user2Taskboard.created_by = request_user
    user2Taskboard.last_modified_by = request_user
    user2Taskboard.save()
    print("Successfully Inserted User2Taskboard into DB: " + user2Taskboard.getDict())


###################################################
### FUNCTION TO REMOVE USER TO TASKBOARD
###################################################
def removeUserFromTaskboard(user, taskboard, request_user):
    user2Taskboard = User2Taskboard.objects.get(user=user, taskboard=taskboard, delete_ind=DELETE_IND_F)
    logical_delete_user2taskboard(user2Taskboard, request_user)
    print("Successfully Removed User2Taskboard: " + user.username + " from " + taskboard.title)


###################################################
### FUNCTION TO UPDATE USER ROLE IN TASKBOARD
###################################################
def updateUserRoleInTaskboard(user, taskboard, user_role, request_user):
    user2Taskboard = User2Taskboard.objects.get(user=user, user_role=USER_ROLE_MEMBER, taskboard=taskboard, delete_ind=DELETE_IND_F)
    user2Taskboard.user_role = user_role
    user2Taskboard.last_modified_by = request_user
    user2Taskboard.save()
    print("Successfully Removed User2Taskboard: " + user2Taskboard.getDict())


def validateAndGenerateTaskboardName(name):
    taskboards = Taskboard.objects.filter(title__istartswith=name, delete_ind=DELETE_IND_F).values_list('title',flat=True).order_by('title')
    if taskboards:
        taskboard_list = list(map(str, list(taskboards)))
        print("====== taskboard_list ===============")
        print(taskboard_list)

        filtered_taskboard_seq_list = []
        regex_pattern = r"(\d+)\b"

        for string in taskboard_list:
            search_str = re.search(regex_pattern, string)
            if (search_str): # have seq number in input name
                if len(string) == len(name):
                    # if input name is exactly the same as existing taskboard string with number 
                    return name
                else:
                    # input name different from existing taskboard string
                    filtered_taskboard_seq_list.append(search_str.group())
            else: # dont have seq number in input name
                filtered_taskboard_seq_list.append("(0)")


        print("====== filtered_taskboard_seq_list ===============")
        print(filtered_taskboard_seq_list)

        if len(filtered_taskboard_seq_list) > 0 :
            max_elem = filtered_taskboard_seq_list[-1]
            max_elem = max_elem.replace('(', '').replace(')','')
            max_elem_int = int(max_elem)
            max_elem_int += 1
            return name + " (" + str(max_elem_int) + ")"
    
    else:
        return name


