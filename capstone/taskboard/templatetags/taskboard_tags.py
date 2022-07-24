from django import template
from django.template.defaultfilters import stringfilter
from ..models import *
from ..constants import *
register = template.Library()

@register.simple_tag
def get_tasks_in_section(sectionId, boardId):
    section = Section.objects.get(id=sectionId)
    taskboard = Taskboard.objects.get(id=boardId)
    tasks = Task.objects.filter(section=section, taskboard=taskboard, delete_ind=DELETE_IND_F)
    return tasks

@register.simple_tag
def get_all_users_in_taskboard(boardId):
    taskboard = Taskboard.objects.get(id=boardId)
    users_user2taskboard = User2Taskboard.objects.filter(taskboard=taskboard, delete_ind=DELETE_IND_F).values_list('user', flat=True)
    users = User.objects.filter(id__in=users_user2taskboard)
    return users
