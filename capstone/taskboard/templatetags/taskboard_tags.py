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