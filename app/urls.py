from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("signup/", views.signup, name="signup"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("project/", views.project_main, name="project"),
    path("client/", views.client, name="client"),
    path("project/create/", views.new_project, name="new_project"),
    path("project/details/", views.project_details, name="project_details"),
    path("client/details/", views.client_details, name="client_details"),
    path("client/manage/", views.manage_client, name="manage_client"),
]