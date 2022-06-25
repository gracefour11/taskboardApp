from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("welcome", views.welcome, name="welcome"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),

    path("taskboards", views.taskboards_view, name="my_taskboards"),
    path("taskboard/create", views.create_taskboard, name="create_taskboard"),
    path("taskboards/load_users", views.load_all_users, name="load_all_users")
]
