from django.urls import path
from . import views
from django.contrib import admin

app_name = 'admindashboard'  # ADD THIS for best practice
urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("districts/", views.districts, name="districts"),
    path("chapters/", views.chapters, name="chapters"),
    path("users/", views.users, name="users"),
    path("edit-requests/", views.edit_requests, name="edit_requests"),
    path("comments/", views.comments, name="comments"),
    path("admin-users/", views.admin_users, name="admin_users"),
    path("permissions/", views.permissions, name="permissions"),
    path("settings/", views.settings, name="settings"),
]