from django.urls import path
from . import views
from django.contrib import admin

app_name = 'users'  # ADD THIS for best practice
urlpatterns = [
    path("login/", views.user_login, name="login"),
    path("forgot_password/", views.forgot_password, name="forgot_password"),
    path("register/", views.register, name="register"),
    path("logout/", views.custom_logout, name="custom_logout"),


]