from django.contrib import admin
from .models import User, Taskboard, User2Taskboard, Section, Task

# Register your models here.
admin.site.register(User)
admin.site.register(Taskboard)
admin.site.register(User2Taskboard)
admin.site.register(Section)
admin.site.register(Task)

