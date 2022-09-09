from django import template
from django.db.models.functions import Coalesce
from ..models import *
from ..constants import *
import datetime

register = template.Library()

@register.simple_tag
def get_uncompleted_tasks_in_section(sectionId, boardId):
    section = Section.objects.get(id=sectionId)
    taskboard = Taskboard.objects.get(id=boardId)
    tasks = Task.objects.filter(section=section, taskboard=taskboard, delete_ind=DELETE_IND_F, complete_ind=COMPLETE_IND_F).order_by(Coalesce('deadline', 'last_modified_dt').asc())
    return tasks

@register.simple_tag
def get_completed_tasks_in_section(sectionId, boardId):
    section = Section.objects.get(id=sectionId)
    taskboard = Taskboard.objects.get(id=boardId)
    tasks = Task.objects.filter(section=section, taskboard=taskboard, delete_ind=DELETE_IND_F, complete_ind=COMPLETE_IND_T).order_by('-last_modified_dt')
    return tasks

@register.simple_tag
def get_all_users_in_taskboard(boardId):
    taskboard = Taskboard.objects.get(id=boardId)
    users_user2taskboard = User2Taskboard.objects.filter(taskboard=taskboard, delete_ind=DELETE_IND_F).values_list('user', flat=True)
    users = User.objects.filter(id__in=users_user2taskboard)
    return users

@register.simple_tag
def get_all_sections_in_taskboard(sectionId, boardId):
    taskboard = Taskboard.objects.get(id=boardId)
    sections = Section.objects.exclude(id=sectionId).filter(taskboard=taskboard, delete_ind=DELETE_IND_F)
    return sections

@register.simple_tag
def get_sections_count_in_taskboard(boardId):
    taskboard = Taskboard.objects.get(id=boardId)
    sections_count = Section.objects.filter(taskboard=taskboard, delete_ind=DELETE_IND_F).count()
    if sections_count > 1:
        return True
    return False

@register.simple_tag
def print_assignee_of_task(assignee, currUser):
    if currUser.id == assignee.id:
        return "Me"
    else:
        return assignee.username

@register.simple_tag
def check_deadline_of_task(taskId):
    task = Task.objects.get(id=taskId)
    if task.deadline == None:
        return False
    return True

@register.simple_tag
def diff_task_deadline_and_today(taskId):
    task = Task.objects.get(id=taskId)
    today = datetime.date.today()
    diff = task.deadline - today
    return diff.days
    # if diff.days < 0: #deadline over
    #     return "R"
    # elif diff.days <= 7: #deadline due in a week 
    #     return "Y"
    # else: #deadline due in more than a week
    #     return "G"
        

    