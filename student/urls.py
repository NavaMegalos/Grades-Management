from django.urls import path
from . import views

app_name = "grades"
urlpatterns = [
    path("upload/", views.upload_grades, name="upload_grades"),
    path("display_grades/", views.display_grades, name="display_grades"),
    path("export_grades/", views.export_grades, name="export_grades"),
]
