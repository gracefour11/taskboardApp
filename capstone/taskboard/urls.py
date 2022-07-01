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
    path("taskboard/<int:boardId>", views.go_to_taskboard, name="go_to_taskboard")
]
