from django.contrib.auth.models import AbstractUser
from django.db import models
import json

class User(AbstractUser):
    pass

class Taskboard(models.Model):
    title = models.CharField(max_length=200, default=None)
    deadline = models.DateField(default=None, null=True)
    type = models.CharField(max_length=100, default=None)
    created_dt = models.DateTimeField(auto_now_add=True, auto_now=False)
    last_modified_dt = models.DateTimeField(auto_now_add=False, auto_now=True)

    def getDict(self):
        dict = self.serialize()
        return json.dumps(dict)
    
    def serialize(self):
        deadlineInDict = self.deadline
        if self.deadline is None:
            deadlineInDict = None
        else:
            deadlineInDict = self.deadline.strftime('%Y-%m-%d')
        return {
            "id": self.id,
            "title": self.title,
            "deadline": deadlineInDict
        }

class User2Taskboard(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name="userId")
    taskboard = models.ForeignKey(Taskboard,on_delete=models.CASCADE,related_name="taskboardId")
    user_role = models.CharField(max_length=10, default=None) #user's role in the taskboard: owner or member
    created_dt = models.DateTimeField(auto_now_add=True, auto_now=False)
    last_modified_dt = models.DateTimeField(auto_now_add=False, auto_now=True)

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