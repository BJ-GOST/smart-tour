from django.urls import path
from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path("sign-up", views.signUp, name="sign-up"),
    path("login", views.login, name="login"),
    path("logout", views.logOut, name="logout")
]