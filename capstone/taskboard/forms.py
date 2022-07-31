from django import forms

TASKBOARD_TYPES = [
    ('IND', 'Individual'),
    ('GRP', 'Group')
]


class CreateEditTaskboardForm(forms.Form):
    taskboard_name = forms.CharField(label="taskboard_name", max_length=100, required=True)
    taskboard_type = forms.CharField(label="taskboard_type", max_length=20, required=True, widget=forms.RadioSelect(choices=TASKBOARD_TYPES, attrs={'onclick': 'showAddMembersView();'}))
    taskboard_members = forms.CharField(label="taskboard_members", max_length=100,required=False)

class DeleteTaskboardForm(forms.Form):
    new_owner_name = forms.CharField(label="new_owner_name", max_length=100, required=False)

class CreateEditTaskForm(forms.Form):
    task_name = forms.CharField(label="task_name", max_length=100, required=True)
    task_deadline = forms.DateField(widget=forms.SelectDateWidget, required=False)
    task_assignee = forms.CharField(label="task_assignee", max_length=100, required=False)
    task_description = forms.CharField(label="task_description", max_length=500, required=True)

class CreateEditSectionForm(forms.Form):
    section_name = forms.CharField(label="section_name", max_length=50, required=True)
