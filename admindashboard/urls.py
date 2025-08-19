from django.urls import path
from . import views
from django.contrib import admin

app_name = 'admindashboard'  # ADD THIS for best practice
urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("districts/", views.districts, name="districts"),
    path("chapters/", views.chapters, name="chapters"),
    path("users/", views.users, name="users"),
    path("users/update-permissions/", views.update_user_permissions, name="update_user_permissions"),
    path("users/delete/", views.delete_user, name="delete_user"),
    path("edit-requests/", views.edit_requests, name="edit_requests"),
    path("comments/", views.comments, name="comments"),
    path("admin-users/", views.admin_users, name="admin_users"),
    path("permissions/", views.permissions, name="permissions"),
    path("settings/", views.settings, name="settings"),
]