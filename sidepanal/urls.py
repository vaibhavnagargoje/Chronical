from django.urls import path
from . import views
app_name = 'sidepanal'  # ADD THIS for best practice
urlpatterns = [
    path("", views.sidepanal_dashboard, name="dashboard"),
    path("dashboard/", views.sidepanal_dashboard, name="sidepanal_dashboard"),
    path("sidepanel/terms/", views.sidepanel_terms, name="sidepanel_terms"),
    path("sidepanel/terms/create/", views.sidepanel_term_create, name="sidepanel_term_create"),
    path("sidepanel/terms/<int:term_id>/edit/", views.sidepanel_term_edit, name="sidepanel_term_edit"),
    path("sidepanel/terms/<int:term_id>/detail/", views.sidepanel_term_detail, name="sidepanel_term_detail"),
    path("sidepanel/terms/delete/", views.sidepanel_term_delete, name="sidepanel_term_delete"),
    path("sidepanel/overrides/", views.sidepanel_overrides, name="sidepanel_overrides"),
    path("sidepanel/overrides/create/", views.sidepanel_override_create, name="sidepanel_override_create"),
    path("sidepanel/overrides/<int:override_id>/edit/", views.sidepanel_override_edit, name="sidepanel_override_edit"),
    path("sidepanel/overrides/<int:override_id>/detail/", views.sidepanel_override_detail, name="sidepanel_override_detail"),
    path("sidepanel/overrides/delete/", views.sidepanel_override_delete, name="sidepanel_override_delete"),
    path("sidepanel/overrides/export/", views.export_overrides, name="export_overrides"),
    path("ajax/chapters/", views.get_chapters_by_district, name="get_chapters_by_district"),
    path("sidepanel/terms/import/", views.import_terms_bulk, name="import_terms_bulk"),
    path("sidepanel/terms/export/", views.export_terms, name="export_terms"),
    

]