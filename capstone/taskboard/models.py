from django.contrib.auth.models import AbstractUser
from django.db import models
import json

class User(AbstractUser):
    def serialize(self):
        return {
            'id': self.id,
            'username': self.username
        }
    
    def getDict(self):
        dict = self.serialize()
        return json.dumps(dict)

class Taskboard(models.Model):
    title = models.CharField(max_length=200, default=None)
    type = models.CharField(max_length=100, default=None)
    created_dt = models.DateTimeField(auto_now_add=True, auto_now=False)
    created_by = models.ForeignKey(User,on_delete=models.CASCADE, related_name='Taskboard_created_by')
    last_modified_dt = models.DateTimeField(auto_now_add=False, auto_now=True)
    last_modified_by = models.ForeignKey(User, on_delete=models.CASCADE,related_name='askboard_last_modified_by')
    delete_ind = models.CharField(max_length=1, default='F')

    def getDict(self):
        dict = self.serialize()
        return json.dumps(dict)
    
    def serialize(self):
        return {
            "id": self.id,
            "title": self.title,
            "type": self.type,
            "last_modified_by": self.last_modified_by.username,
            "last_modified_dt": self.last_modified_dt.strftime('%Y-%m-%d'),
            "created_by": self.created_by.username,
            "created_dt": self.created_dt.strftime('%Y-%m-%d')
        }

class User2Taskboard(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name="userId")
    taskboard = models.ForeignKey(Taskboard,on_delete=models.CASCADE,related_name="taskboardId", related_query_name="user2taskboard")
    user_role = models.CharField(max_length=10, default=None) #user's role in the taskboard: owner or member
    created_dt = models.DateTimeField(auto_now_add=True, auto_now=False)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE,related_name='User2Taskboard_created_by')
    last_modified_dt = models.DateTimeField(auto_now_add=False, auto_now=True)
    last_modified_by = models.ForeignKey(User, on_delete=models.CASCADE,related_name='User2Taskboard_last_modified_by')
    delete_ind = models.CharField(max_length=1, default='F')

    def serialize(self):
        return {
            "id": self.id,
            "userId": self.user.id,
            "taskboardId": self.taskboard.id,
            "userRole": self.user_role
        }

    def getDict(self):
        dict = self.serialize()
        return json.dumps(dict)

class Section(models.Model):
    taskboard = models.ForeignKey(Taskboard,on_delete=models.CASCADE,related_name="taskboardForSection", related_query_name="taskboardForSection") 
    name = models.CharField(max_length=50, default=None)
    created_dt = models.DateTimeField(auto_now_add=True, auto_now=False)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE,related_name='Section_created_by')
    last_modified_dt = models.DateTimeField(auto_now_add=False, auto_now=True)
    last_modified_by = models.ForeignKey(User, on_delete=models.CASCADE,related_name='Section_last_modified_by')
    delete_ind = models.CharField(max_length=1, default='F')

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "taskboardId": self.taskboard.id,
            "last_modified_by": self.last_modified_by.username,
            "last_modified_dt": self.last_modified_dt.strftime('%Y-%m-%d'),
            "created_by": self.created_by.username,
            "created_dt": self.created_dt.strftime('%Y-%m-%d')
        }

class Task(models.Model):
    taskboard = models.ForeignKey(Taskboard,on_delete=models.CASCADE,related_name="taskboardForTask", related_query_name="taskboardForTask")
    name = models.CharField(max_length=50, default=None)
    description = models.CharField(max_length=200, default=None)
    assignee = models.ForeignKey(User, on_delete=models.CASCADE,related_name='asignee')
    section = models.ForeignKey(Section, on_delete=models.CASCADE,related_name="sectionForTask", related_query_name="sectionForTask")
    deadline = models.DateField(default=None, null=True)
    created_dt = models.DateTimeField(auto_now_add=True, auto_now=False)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE,related_name='Task_created_by')
    last_modified_dt = models.DateTimeField(auto_now_add=False, auto_now=True)
    last_modified_by = models.ForeignKey(User, on_delete=models.CASCADE,related_name='Task_last_modified_by')
    delete_ind = models.CharField(max_length=1, default='F')

    def serialize(self):
        deadlineInDict = self.deadline
        if self.deadline is None:
            deadlineInDict = None
        else:
            deadlineInDict = self.deadline.strftime('%Y-%m-%d')
        return {
            "id": self.id,
            "name": self.name,
            "deadline": deadlineInDict,
            "section": self.section.id,
            "assignee": self.assignee.username,
            "description": self.description,
            "last_modified_by": self.last_modified_by.username,
            "last_modified_dt": self.last_modified_dt.strftime('%Y-%m-%d'),
            "created_by": self.created_by.username,
            "created_dt": self.created_dt.strftime('%Y-%m-%d')
        }

