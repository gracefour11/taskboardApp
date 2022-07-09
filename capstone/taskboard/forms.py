from django import forms
from .models import User

TASKBOARD_TYPES = [
    ('IND', 'Individual'),
    ('GRP', 'Group')
]

class CreateEditTaskboardForm(forms.Form):
    taskboard_name = forms.CharField(label="taskboard_name", max_length=100, required=True)
    taskboard_deadline = forms.DateTimeField(widget=forms.SelectDateWidget, required=False)
    taskboard_type = forms.CharField(label="taskboard_type", max_length=20, required=True, widget=forms.RadioSelect(choices=TASKBOARD_TYPES, attrs={'onclick': 'showAddMembersView();'}))
    taskboard_members = forms.CharField(label="taskboard_members", max_length=100,required=False)

class DeleteTaskboardForm(forms.Form):
    new_owner = forms.CharField(label="new_owner_name", max_length=100, required=True)

class CreateEditTaskForm(forms.Form):
    title = forms.CharField(label="title", max_length=100, required=True)
    deadline = forms.DateTimeField(widget=forms.SelectDateWidget, required=False)
    asignee = forms.CharField(label="asignee", max_length=100, required=False)
    section = forms.CharField(label="section", max_length=100, required=True)
    contents = forms.CharField(label="contents", max_length=500, required=True)