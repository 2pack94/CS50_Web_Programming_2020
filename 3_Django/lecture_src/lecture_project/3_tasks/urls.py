from django.urls import path

from . import views

# use an app name to reference the URL names unambiguously. Avoids URL name clashes with other apps.
app_name = "tasks"
urlpatterns = [
    path("", views.index, name="index"),
    path("add", views.add, name="add"),
]
