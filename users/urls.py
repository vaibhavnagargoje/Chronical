from django.urls import path
from . import views
from django.contrib import admin

app_name = 'users'  # ADD THIS for best practice
urlpatterns = [
    path("login/", views.user_login, name="login"),
    path("forgot_password/", views.forgot_password, name="forgot_password"),
    path("reset_password/<str:token>/", views.reset_password, name="reset_password"),
    path("register/", views.register, name="register"),
    path("verify_otp/", views.verify_otp, name="verify_otp"),
    path("registration_success/", views.registration_success, name="registration_success"),
    path("logout/", views.custom_logout, name="custom_logout"),
    path("login_success/", views.login_success, name="login_success"),


    path("profile/", views.user_profile, name="user_profile"),

]