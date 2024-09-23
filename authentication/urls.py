from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("api/user/login", views.login, name="login"),
    path("api/user/logout", views.logout, name="logout"),
    path("callback", views.callback, name="callback"),


]