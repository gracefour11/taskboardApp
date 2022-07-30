from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("welcome", views.welcome, name="welcome"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),

    path("taskboard/create", views.create_taskboard, name="create_taskboard"),
    path("taskboards/load_users", views.load_all_users, name="load_all_users"),
    path("taskboard/<int:boardId>", views.go_to_taskboard, name="go_to_taskboard"),
    path("taskboard/<int:boardId>/edit", views.edit_taskboard, name="edit_taskboard"),
    path("taskboard/<int:boardId>/delete", views.delete_taskboard, name="delete_taskboard"),
    path("taskboard/<int:boardId>/view", views.get_taskboard_contents, name="get_taskboard_contents"),

    path("taskboard/<int:boardId>/section/create", views.create_section, name="create_section"),
    path("taskboard/<int:boardId>/section/<int:sectionId>/edit", views.edit_section, name="edit_section"),
    path("taskboard/<int:boardId>/section/<int:sectionId>/delete", views.delete_section, name="delete_section"),

    path("taskboard/<int:boardId>/section/<int:sectionId>/task/create", views.create_task, name="create_task"),
    path("taskboard/<int:boardId>/section/<int:sectionId>/task/<int:taskId>", views.get_task_contents, name="get_task_contents"),
    path("taskboard/<int:boardId>/section/<int:sectionId>/task/<int:taskId>/edit", views.edit_task, name="edit_task"),
    path("taskboard/<int:boardId>/section/<int:sectionId>/task/<int:taskId>/delete", views.delete_task, name="delete_task"),
    path("taskboard/<int:boardId>/section/<int:sectionId>/task/<int:taskId>/complete", views.complete_task, name="complete_task"),
    path("taskboard/<int:boardId>/section/<int:sectionId>/task/<int:taskId>/move", views.move_task, name="move_task"),
]
