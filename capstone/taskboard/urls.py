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
    path("taskboard/<int:boardId>/view", views.get_taskboard_contents, name="view_taskboard"),

    path("taskboard/<int:boardId>/section/create", views.create_section, name="create_section"),
    path("taskboard/<int:boardId>/section/<int:sectionId>/edit", views.edit_section, name="edit_section"),
    path("taskboard/<int:boardId>/section/<int:sectionId>/delete", views.delete_section, name="delete_section"),
]
